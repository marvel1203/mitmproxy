"""将HTTP请求重定向到另一个服务器。"""

from mitmproxy import http


def request(flow: http.HTTPFlow) -> None:
    # pretty_host会考虑请求的"Host"头部信息，
    # 这在透明代理模式下特别有用，因为在透明模式下我们通常只能获取IP地址。
    if flow.request.pretty_host == "example.org":
        flow.request.host = "mitmproxy.org"
