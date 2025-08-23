"""响应配置变更。"""

from typing import Optional

from mitmproxy import ctx
from mitmproxy import exceptions


class AddHeader:
    def load(self, loader):
        loader.add_option(
            name="addheader",
            typespec=Optional[int],
            default=None,
            help="向响应添加一个头部",
        )

    def configure(self, updates):
        if "addheader" in updates:
            if ctx.options.addheader is not None and ctx.options.addheader > 100:
                raise exceptions.OptionsError("addheader必须小于等于100")

    def response(self, flow):
        if ctx.options.addheader is not None:
            flow.response.headers["addheader"] = str(ctx.options.addheader)


addons = [AddHeader()]
