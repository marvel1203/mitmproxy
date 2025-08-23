"""
使用简化脚本语法的 mitmproxy 插件示例。
"""


def request(flow):
    flow.request.headers["myheader"] = "value"
