"""
关闭mitmproxy实例的简单方法，用于停止所有操作。

用法：

    mitmproxy -s shutdown.py

    然后发送一个HTTP请求来触发关闭：
    curl --proxy localhost:8080 http://example.com/path
"""

import logging

from mitmproxy import ctx
from mitmproxy import http


def request(flow: http.HTTPFlow) -> None:
    # 一个随机条件，使这个例子更具交互性
    if flow.request.pretty_url == "http://example.com/path":
        logging.info("正在关闭所有内容...")
        ctx.master.shutdown()
