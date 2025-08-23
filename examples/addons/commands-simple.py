"""
为 mitmproxy 命令行添加自定义命令的示例。
"""

import logging

from mitmproxy import command


class MyAddon:
    def __init__(self):
        self.num = 0

    @command.command("myaddon.inc")
    def inc(self) -> None:
        self.num += 1
        logging.info(f"num = {self.num}")


addons = [MyAddon()]
