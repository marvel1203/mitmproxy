from mitmproxy import contentviews


class SwapCase(contentviews.Contentview):
    def prettify(self, data: bytes, metadata: contentviews.Metadata) -> str:
        # 将内容大小写反转后解码为字符串
        return data.swapcase().decode()

    def render_priority(self, data: bytes, metadata: contentviews.Metadata) -> float:
        # 如果内容类型以"text/example"开头，则优先显示本视图
        if metadata.content_type and metadata.content_type.startswith("text/example"):
            return 2  # 返回大于1的值，确保自动选择自定义视图
        else:
            return 0


contentviews.add(SwapCase)
