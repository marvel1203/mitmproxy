"""
此脚本简单打印出所有接收到的HTTP尾部头信息(Trailers)。

HTTP请求和响应可以包含在主体完全传输后发送的尾部头信息。这些尾部头需要在初始头信息中
按名称提前声明，这样接收端才能等待并在读取主体后接收它们。
"""

from mitmproxy import http
from mitmproxy.http import Headers


def request(flow: http.HTTPFlow):
    if flow.request.trailers:
        print("检测到HTTP尾部头信息！请求包含:", flow.request.trailers)

    if flow.request.path == "/inject_trailers":
        if flow.request.is_http10:
            # HTTP/1.0不支持尾部头信息
            return
        elif flow.request.is_http11:
            if not flow.request.content:
                # 避免在GET请求上发送主体或发送带尾部头信息的0字节分块主体。
                # 否则某些服务器会返回400 Bad Request。
                return
            # HTTP 1.1要求使用transfer-encoding: chunked来发送尾部头信息
            flow.request.headers["transfer-encoding"] = "chunked"
        # HTTP 2+在所有请求/响应上都支持尾部头信息

        flow.request.headers["trailer"] = "x-my-injected-trailer-header"
        flow.request.trailers = Headers([(b"x-my-injected-trailer-header", b"foobar")])
        print("注入了一个新的请求尾部头信息...", flow.request.headers["trailer"])


def response(flow: http.HTTPFlow):
    assert flow.response
    if flow.response.trailers:
        print("检测到HTTP尾部头信息！响应包含:", flow.response.trailers)

    if flow.request.path == "/inject_trailers":
        if flow.request.is_http10:
            return
        elif flow.request.is_http11:
            if not flow.response.content:
                return
            flow.response.headers["transfer-encoding"] = "chunked"

        flow.response.headers["trailer"] = "x-my-injected-trailer-header"
        flow.response.trailers = Headers([(b"x-my-injected-trailer-header", b"foobar")])
        print("注入了一个新的响应尾部头信息...", flow.response.headers["trailer"])
