"""
向运行中的WebSocket连接注入消息。

此示例展示如何向正在运行的WebSocket连接中注入消息。
"""

import asyncio

from mitmproxy import ctx
from mitmproxy import http

# 简单示例：作为事件响应注入消息


def websocket_message(flow: http.HTTPFlow):
    assert flow.websocket is not None  # 让类型检查器开心
    last_message = flow.websocket.messages[-1]
    if last_message.is_text and "secret" in last_message.text:
        last_message.drop()
        ctx.master.commands.call(
            "inject.websocket", flow, last_message.from_client, b"ssssssh"
        )


# 复杂示例：安排定期计时器


async def inject_async(flow: http.HTTPFlow):
    msg = "hello from mitmproxy! "
    assert flow.websocket is not None  # 让类型检查器开心
    while flow.websocket.timestamp_end is None:
        ctx.master.commands.call("inject.websocket", flow, True, msg.encode())
        await asyncio.sleep(1)
        msg = msg[1:] + msg[:1]


tasks = set()


def websocket_start(flow: http.HTTPFlow):
    # 我们需要保持对任务的引用，否则它将被垃圾回收。
    t = asyncio.create_task(inject_async(flow))
    tasks.add(t)
    t.add_done_callback(tasks.remove)
