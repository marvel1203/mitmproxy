"""
添加一个新的mitmproxy选项。

用法：

    mitmproxy -s options-simple.py --set addheader=true
"""

from mitmproxy import ctx


class AddHeader:
    def __init__(self):
        self.num = 0

    def load(self, loader):
        loader.add_option(
            name="addheader",
            typespec=bool,
            default=False,
            help="向响应添加一个计数头部",
        )

    def response(self, flow):
        if ctx.options.addheader:
            self.num = self.num + 1
            flow.response.headers["count"] = str(self.num)


addons = [AddHeader()]
