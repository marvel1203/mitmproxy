from collections.abc import Sequence
from typing import Optional

from mitmproxy import optmanager

CONF_DIR = "~/.mitmproxy"
CONF_BASENAME = "mitmproxy"
CONTENT_VIEW_LINES_CUTOFF = 512
KEY_SIZE = 2048


class Options(optmanager.OptManager):
    def __init__(self, **kwargs) -> None:
        super().__init__()
        self.add_option(
            "server", bool, True, "启动代理服务器。默认启用。"
        )
        self.add_option(
            "showhost",
            bool,
            False,
            """使用 Host 头部构建用于显示的 URL。

            默认禁用此选项，因为恶意应用可能发送误导性的 host 头部以规避你的分析。如果这不是问题，可以启用此选项以获得更好的流量显示。""",
        )
        self.add_option(
            "show_ignored_hosts",
            bool,
            False,
            """
            即使未进行 TLS 拦截，也在 UI 中记录被忽略的流量。
            此选项会将被忽略流的内容保存在内存中，可能会大幅增加内存使用。
            未来版本将修复此问题，默认记录被忽略流，并移除此选项。
            """,
        )

        # 代理相关选项
        self.add_option(
            "add_upstream_certs_to_client_chain",
            bool,
            False,
            """
            将上游服务器的所有证书作为额外证书添加到将提供给代理客户端的证书链中。
            """,
        )
        self.add_option(
            "confdir",
            str,
            CONF_DIR,
            "mitmproxy 配置文件的默认位置。",
        )
        self.add_option(
            "certs",
            Sequence[str],
            [],
            """
            SSL 证书，格式为“[domain=]path”。domain 可包含通配符，若未指定则为“*”。
            path 处的文件为 PEM 格式证书。如果包含私钥则使用，否则使用 confdir 下的默认私钥。
            PEM 文件应包含完整证书链，叶子证书为第一个条目。
            """,
        )
        self.add_option(
            "cert_passphrase",
            Optional[str],
            None,
            """
            用于解密 --cert 选项中私钥的密码。

            注意：在命令行传递 cert_passphrase 会使密码在系统进程列表中可见。建议在 config.yaml 中指定以避免泄露。
            """,
        )
        self.add_option(
            "client_certs", Optional[str], None, "客户端证书文件或目录。"
        )
        self.add_option(
            "ignore_hosts",
            Sequence[str],
            [],
            """
            忽略主机并直接转发所有流量，不做处理。
            透明模式下建议使用 IP 地址（段），非主机名。常规模式下仅忽略 SSL 流量，需使用主机名。
            支持正则表达式，匹配 IP 或主机名。
            """,
        )
        self.add_option("allow_hosts", Sequence[str], [], "与 --ignore-hosts 相反。")
        self.add_option(
            "listen_host",
            str,
            "",
            "绑定代理服务器的地址（可被各模式单独覆盖，见 `mode` 选项）。",
        )
        self.add_option(
            "listen_port",
            Optional[int],
            None,
            "绑定代理服务器的端口（可被各模式单独覆盖，见 `mode` 选项）。默认端口依赖于模式。常规 HTTP 代理默认 8080 端口。",
        )
        self.add_option(
            "mode",
            Sequence[str],
            ["regular"],
            """
            要启动的代理服务器类型。可多次传递。

            支持 "regular"（HTTP）、"transparent"、"socks5"、"reverse:SPEC"、"upstream:SPEC" 和 "wireguard[:PATH]"。
            reverse/upstream 模式下，SPEC 为 "http[s]://host[:port]"。WireGuard 模式下，PATH 可指向密钥文件，不存在则启动时创建。

            可追加 `@listen_port` 或 `@listen_host:listen_port`，为特定代理模式覆盖监听地址或端口。部分功能（如回放）会使用第一个模式确定上游服务器。
            """,
        )
        self.add_option(
            "upstream_cert",
            bool,
            True,
            "连接上游服务器以获取证书详情。",
        )

        self.add_option(
            "http2",
            bool,
            True,
            "启用/禁用 HTTP/2 支持。默认启用。",
        )
        self.add_option(
            "http2_ping_keepalive",
            int,
            58,
            """
            HTTP/2 连接空闲超过指定秒数时发送 PING 帧，防止远端关闭连接。
            设为 0 可禁用此功能。
            """,
        )
        self.add_option(
            "http3",
            bool,
            True,
            "启用/禁用 QUIC 和 HTTP/3 支持。默认启用。",
        )
        self.add_option(
            "http_connect_send_host_header",
            bool,
            True,
            "CONNECT 请求中包含 host 头。默认启用。",
        )
        self.add_option(
            "websocket",
            bool,
            True,
            "启用/禁用 WebSocket 支持。默认启用。",
        )
        self.add_option(
            "rawtcp",
            bool,
            True,
            "启用/禁用原始 TCP 连接。默认启用。",
        )
        self.add_option(
            "ssl_insecure",
            bool,
            False,
            """不验证上游服务器 SSL/TLS 证书。

            启用后将跳过证书校验，mitmproxy 本身将易受 TLS 中间人攻击。""",
        )
        self.add_option(
            "ssl_verify_upstream_trusted_confdir",
            Optional[str],
            None,
            """
            上游服务器验证用的受信任 CA 证书目录，需用 c_rehash 工具预处理。
            """,
        )
        self.add_option(
            "ssl_verify_upstream_trusted_ca",
            Optional[str],
            None,
            "PEM 格式的受信任 CA 证书路径。",
        )
        self.add_option(
            "tcp_hosts",
            Sequence[str],
            [],
            """
            匹配指定主机的通用 TCP SSL 代理模式。
            类似 --ignore-hosts，但会拦截 SSL 连接。
            通信内容在详细日志模式下输出。
            """,
        )
        self.add_option(
            "udp_hosts",
            Sequence[str],
            [],
            """
            匹配指定主机的通用 UDP SSL 代理模式。
            类似 --ignore-hosts，但会拦截 SSL 连接。
            通信内容在详细日志模式下输出。
            """,
        )
        self.add_option(
            "content_view_lines_cutoff",
            int,
            CONTENT_VIEW_LINES_CUTOFF,
            """
            流内容视图行数限制。默认启用以加快流浏览速度。
            """,
        )
        self.add_option(
            "key_size",
            int,
            KEY_SIZE,
            """
            证书和 CA 的 TLS 密钥长度。
            """,
        )
        self.add_option(
            "protobuf_definitions",
            Optional[str],
            None,
            "用于 Protobuf 美化显示字段名的 .proto 文件路径。",
        )
        self.add_option(
            "tcp_timeout",
            int,
            600,
            """
            Timeout in seconds for inactive TCP connections. Connections will be closed after this period of inactivity.
            """,
        )

        self.update(**kwargs)
