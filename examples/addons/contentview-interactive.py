from mitmproxy import contentviews


class InteractiveSwapCase(contentviews.InteractiveContentview):
    def prettify(
        self,
        data: bytes,
        metadata: contentviews.Metadata,
    ) -> str:
        # 将内容大小写反转后解码为字符串
        return data.swapcase().decode()

    def reencode(
        self,
        prettified: str,
        metadata: contentviews.Metadata,
    ) -> bytes:
        # 将字符串再次大小写反转并编码为字节
        return prettified.encode().swapcase()


contentviews.add(InteractiveSwapCase)
