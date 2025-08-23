"""从代理直接发送响应，而不将请求发送到远程服务器。"""

from mitmproxy import http


def request(flow: http.HTTPFlow) -> None:
    if flow.request.pretty_url == "http://example.com/path":
        flow.response = http.Response.make(
            200,  # (可选) 状态码
            b"Hello World",  # (可选) 内容
            {"Content-Type": "text/html"},  # (可选) 头部
        )
