"""向mitmproxy的事件日志发送消息。"""

import logging

from mitmproxy.addonmanager import Loader
from mitmproxy.log import ALERT

logger = logging.getLogger(__name__)


def load(loader: Loader):
    logger.info("这是一些信息性文本。")
    logger.warning("这是一个警告。")
    logger.error("这是一个错误。")
    logger.log(
        ALERT,
        "这是一个提醒。它与info具有相同的紧急程度，但也会在状态栏中弹出显示。",
    )
