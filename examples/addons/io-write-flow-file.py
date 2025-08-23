"""
生成mitmproxy流量dump文件。

此脚本演示如何生成mitmproxy dump文件，
效果类似于向mitmproxy传递`-w`参数。
与`-w`参数不同，这种方法可以让你完全控制
哪些流量应该被保存，还允许你轮换文件或同时
记录到多个文件。
"""

import os
import random
from typing import BinaryIO

from mitmproxy import http
from mitmproxy import io


class Writer:
    def __init__(self) -> None:
        # 我们使用环境变量来保持示例尽可能简单，
        # 在实际应用中，考虑将此实现为mitmproxy选项。
        filename = os.getenv("MITMPROXY_OUTFILE", "out.mitm")
        self.f: BinaryIO = open(filename, "wb")
        self.w = io.FlowWriter(self.f)

    def response(self, flow: http.HTTPFlow) -> None:
        if random.choice([True, False]):
            self.w.add(flow)

    def done(self):
        self.f.close()


addons = [Writer()]
