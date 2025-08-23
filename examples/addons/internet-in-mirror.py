"""
镜像翻转所有网页。

对生活在"地球另一端"的人特别有用。
"""

from mitmproxy import http


def response(flow: http.HTTPFlow) -> None:
    if flow.response and flow.response.content:
        flow.response.content = flow.response.content.replace(
            b"</head>", b"<style>body {transform: scaleX(-1);}</style></head>"
        )
