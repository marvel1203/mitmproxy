"""
在mitmproxy中托管WSGI应用。

此示例展示了如何将WSGI应用嫁接到mitmproxy上。在这个
实例中，我们使用Flask框架(http://flask.pocoo.org/)来展示
一个最简单的页面。
"""

from flask import Flask

from mitmproxy.addons import asgiapp

app = Flask("proxapp")


@app.route("/")
def hello_world() -> str:
    return "Hello World!"


addons = [
    # 在魔法域名"example.com"的80端口上托管应用。对这个
    # 域名和端口组合的请求现在将被路由到WSGI应用实例。
    asgiapp.WSGIApp(app, "example.com", 80),
    # TLS也能工作，但由于mitmproxy的设计，魔法域名需要能从mitmproxy机器上解析。
    # mitmproxy将连接到该域名并使用其证书，但不会发送任何数据。
    # 通过使用`--set upstream_cert=false`和`--set connection_strategy_lazy`参数，将改用本地证书。
    # asgiapp.WSGIApp(app, "example.com", 443),
]
