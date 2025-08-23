"""
接收HTTP请求并以修改后的参数重放的示例。
"""

from mitmproxy import ctx


def request(flow):
    # 避免对已重放的请求再次重放，防止死循环
    if flow.is_replay == "request":
        return
    flow = flow.copy()
    # 仅交互式工具有视图。如果有，添加一个重复的流量条目
    if "view" in ctx.master.addons:
        ctx.master.commands.call("view.flows.duplicate", [flow])
    flow.request.path = "/changed"
    ctx.master.commands.call("replay.client", [flow])
