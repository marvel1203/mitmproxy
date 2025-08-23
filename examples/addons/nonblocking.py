"""
使用async或@concurrent使事件钩子变为非阻塞。
"""

import asyncio
import logging
import time

from mitmproxy.script import concurrent

# 在异步和基于线程的替代方案之间切换。
if True:
    # 钩子可以是异步的，这允许钩子调用异步函数并执行异步I/O
    # 而不会阻塞其他请求。对于新插件，这通常是首选方法。
    async def request(flow):
        logging.info(f"处理请求: {flow.request.host}{flow.request.path}")
        await asyncio.sleep(5)
        logging.info(f"开始请求: {flow.request.host}{flow.request.path}")

else:
    # 另一个选择是使用@concurrent，它在自己的线程中启动钩子。
    # 请注意，这通常会导致竞态条件，如果不是必需的，会降低性能。
    @concurrent  # 移除此装饰器使其同步执行，观察会发生什么
    def request(flow):
        logging.info(f"处理请求: {flow.request.host}{flow.request.path}")
        time.sleep(5)
        logging.info(f"开始请求: {flow.request.host}{flow.request.path}")
