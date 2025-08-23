"""修改HTTP表单提交。"""

from mitmproxy import http


def request(flow: http.HTTPFlow) -> None:
    if flow.request.urlencoded_form:
        # 如果已有表单，可以直接向字典中添加项目：
        flow.request.urlencoded_form["mitmproxy"] = "rocks"
    else:
        # 也可以直接传递新的表单数据。
        # 这会设置适当的内容类型并覆盖请求体。
        flow.request.urlencoded_form = [("foo", "bar")]  # type: ignore[assignment]
