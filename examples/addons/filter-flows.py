"""
在脚本中使用mitmproxy的过滤器模式。
"""

from __future__ import annotations

import logging

from mitmproxy import flowfilter
from mitmproxy import http
from mitmproxy.addonmanager import Loader


class Filter:
    filter: flowfilter.TFilter

    def configure(self, updated):
        if "flowfilter" in updated:
            self.filter = flowfilter.parse(".")

    def load(self, loader: Loader):
        loader.add_option("flowfilter", str, "", "检查流量是否匹配过滤器。")

    def response(self, flow: http.HTTPFlow) -> None:
        if flowfilter.match(self.filter, flow):
            logging.info("流量匹配过滤器:")
            logging.info(flow)


addons = [Filter()]
