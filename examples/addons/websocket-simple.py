"""处理WebSocket连接中的单个消息。"""

import logging
import re

from mitmproxy import http


def websocket_message(flow: http.HTTPFlow):
    assert flow.websocket is not None  # 让类型检查器开心
    # 获取最新的消息
    message = flow.websocket.messages[-1]

    # 消息是由客户端还是服务器发送的？
    if message.from_client:
        logging.info(f"客户端发送了一条消息: {message.content!r}")
    else:
        logging.info(f"服务器发送了一条消息: {message.content!r}")

    # 操作消息内容
    message.content = re.sub(rb"^Hello", b"HAPPY", message.content)

    if b"FOOBAR" in message.content:
        # 丢弃消息，不发送到另一端
        message.drop()
