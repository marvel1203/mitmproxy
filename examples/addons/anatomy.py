"""
mitmproxy 插件的基本骨架示例。

运行方式：mitmproxy -s anatomy.py
"""

import logging


class Counter:
    def __init__(self):
        self.num = 0

    def request(self, flow):
        self.num = self.num + 1
        logging.info("已捕获 %d 个流量" % self.num)


addons = [Counter()]
