"""修改HTTP查询参数。"""

from mitmproxy import http


def request(flow: http.HTTPFlow) -> None:
    flow.request.query["mitmproxy"] = "rocks"
