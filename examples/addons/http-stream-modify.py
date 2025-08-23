"""
修改流式响应。

一般来说，我们建议*不要*对需要修改的消息使用流式处理。
修改流式响应很棘手且容易出错：
    - 如果传输编码不是分块的，你不能简单地更改内容长度。
    - 如果你想替换所有出现的"foobar"，请确保捕获这种情况：
      一个数据块以[...]foo"结尾，而下一个数据块以"bar[...]开头。
"""

from collections.abc import Iterable


def modify(data: bytes) -> bytes | Iterable[bytes]:
    """
    此函数将在每个请求/响应体数据块到达代理时被调用，
    并在消息结束时使用空字节参数(b"")调用一次。

    它可以返回字节或字节的可迭代对象（这将导致多个HTTP/2数据帧）。
    """
    return data.replace(b"foo", b"bar")


def responseheaders(flow):
    flow.response.stream = modify
