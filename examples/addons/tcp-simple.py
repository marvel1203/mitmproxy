"""
处理TCP连接中的单个消息。

此脚本将完整出现的"foo"替换为"bar"，并为每条消息打印各种详细信息。
请注意，TCP是基于流的，而*不是*基于消息的。mitmproxy将流内容拆分为
socket.recv()接收到的"消息"。这是相当任意的，不应该被依赖。
但是，作为快速解决方案，它有时已经足够好。

示例调用:

    mitmdump --tcp-hosts ".*" -s examples/tcp-simple.py
"""

import logging

from mitmproxy import tcp
from mitmproxy.utils import strutils


def tcp_message(flow: tcp.TCPFlow):
    message = flow.messages[-1]
    message.content = message.content.replace(b"foo", b"bar")

    logging.info(
        f"tcp_message[from_client={message.from_client}), content={strutils.bytes_to_escaped_str(message.content)}]"
    )
