import asyncio
import logging

from . import ctx as mitmproxy_ctx
from .addons import termlog
from .proxy.mode_specs import ReverseMode
from .utils import asyncio_utils
from mitmproxy import addonmanager
from mitmproxy import command
from mitmproxy import eventsequence
from mitmproxy import hooks
from mitmproxy import http
from mitmproxy import log
from mitmproxy import options

logger = logging.getLogger(__name__)


class Master:
    """
    主控制器类，负责mitmproxy主事件循环。
    主要职责：
    - 初始化配置、插件、命令管理器
    - 启动和关闭事件循环
    - 触发运行/完成钩子
    - 加载和重放流量
    """

    event_loop: asyncio.AbstractEventLoop
    _termlog_addon: termlog.TermLog | None = None

    def __init__(
        self,
        opts: options.Options | None,
        event_loop: asyncio.AbstractEventLoop | None = None,
        with_termlog: bool = False,
    ):
        """
        初始化主控制器
        :param opts: 配置选项
        :param event_loop: 异步事件循环
        :param with_termlog: 是否启用终端日志
        """
        self.options: options.Options = opts or options.Options()
        self.commands = command.CommandManager(self)
        self.addons = addonmanager.AddonManager(self)

        if with_termlog:
            self._termlog_addon = termlog.TermLog()
            self.addons.add(self._termlog_addon)

        self.log = log.Log(self)  # deprecated, do not use.
        self._legacy_log_events = log.LegacyLogEvents(self)
        self._legacy_log_events.install()

        # We expect an active event loop here already because some addons
        # may want to spawn tasks during the initial configuration phase,
        # which happens before run().
        self.event_loop = event_loop or asyncio.get_running_loop()
        self.should_exit = asyncio.Event()
        mitmproxy_ctx.master = self
        mitmproxy_ctx.log = self.log  # deprecated, do not use.
        mitmproxy_ctx.options = self.options

    async def run(self) -> None:
        """
        运行代理服务器主循环。
        步骤：
        - 设置异常处理器
        - 启动代理服务器
        - 等待退出信号
        """
        with (
            asyncio_utils.install_exception_handler(self._asyncio_exception_handler),
            asyncio_utils.set_eager_task_factory(),
        ):
            self.should_exit.clear()

            # Can we exit before even bringing up servers?
            if ec := self.addons.get("errorcheck"):
                await ec.shutdown_if_errored()
            if ps := self.addons.get("proxyserver"):
                # This may block for some proxy modes, so we also monitor should_exit.
                await asyncio.wait(
                    [
                        asyncio_utils.create_task(
                            ps.setup_servers(), name="setup_servers", keep_ref=False
                        ),
                        asyncio_utils.create_task(
                            self.should_exit.wait(), name="should_exit", keep_ref=False
                        ),
                    ],
                    return_when=asyncio.FIRST_COMPLETED,
                )
                if self.should_exit.is_set():
                    return
                # Did bringing up servers fail?
                if ec := self.addons.get("errorcheck"):
                    await ec.shutdown_if_errored()

            try:
                await self.running()
                # Any errors in the final part of startup?
                if ec := self.addons.get("errorcheck"):
                    await ec.shutdown_if_errored()
                    ec.finish()

                await self.should_exit.wait()
            finally:
                # if running() was called, we also always want to call done().
                # .wait might be cancelled (e.g. by sys.exit), so  this needs to be in a finally block.
                await self.done()

    def shutdown(self):
        """
        关闭代理服务器（线程安全）
        """
        # We may add an exception argument here.
        self.event_loop.call_soon_threadsafe(self.should_exit.set)

    async def running(self) -> None:
        """
        触发运行状态钩子事件
        """
        await self.addons.trigger_event(hooks.RunningHook())

    async def done(self) -> None:
        """
        触发完成状态钩子事件并清理资源
        """
        await self.addons.trigger_event(hooks.DoneHook())
        self._legacy_log_events.uninstall()
        if self._termlog_addon is not None:
            self._termlog_addon.uninstall()

    def _asyncio_exception_handler(self, loop, context) -> None:
        try:
            exc: Exception = context["exception"]
        except KeyError:
            logger.error(f"Unhandled asyncio error: {context}")
        else:
            if isinstance(exc, OSError) and exc.errno == 10038:
                return  # suppress https://bugs.python.org/issue43253
            logger.error(
                "Unhandled error in task.",
                exc_info=(type(exc), exc, exc.__traceback__),
            )

    async def load_flow(self, f):
        """
        加载并重放流量数据
        :param f: 要加载的流量对象
        """

        if (
            isinstance(f, http.HTTPFlow)
            and len(self.options.mode) == 1
            and self.options.mode[0].startswith("reverse:")
        ):
            # When we load flows in reverse proxy mode, we adjust the target host to
            # the reverse proxy destination for all flows we load. This makes it very
            # easy to replay saved flows against a different host.
            # We may change this in the future so that clientplayback always replays to the first mode.
            mode = ReverseMode.parse(self.options.mode[0])
            assert isinstance(mode, ReverseMode)
            f.request.host, f.request.port, *_ = mode.address
            f.request.scheme = mode.scheme

        for e in eventsequence.iterate(f):
            await self.addons.handle_lifecycle(e)
