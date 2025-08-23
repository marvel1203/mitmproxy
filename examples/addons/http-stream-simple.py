"""
选择哪些响应应该被流式处理。

为所有HTTP流量启用响应流式处理。
这相当于向mitmproxy传递`--set stream_large_bodies=1`参数。
"""


def responseheaders(flow):
    """
    为所有响应启用流式处理。
    这相当于向mitmproxy传递`--set stream_large_bodies=1`参数。
    """
    flow.response.stream = True
