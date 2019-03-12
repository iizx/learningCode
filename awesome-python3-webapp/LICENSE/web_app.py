import logging; logging.basicConfig(level=logging.INFO)
import os,json,time,asyncio
from datetime import datetime
from aiohttp import web
#导入相关的包，其中logging为系统日志；aiohttp是异步web包；asyncio为异步io包
#定义请求处理函数
def index(request):
    return web.Response(body='<h1>Awesome!!</h1>'.encode('UTF-8'),content_type='text/html')

#异步web请求
#采用装饰器
@asyncio.coroutine
def init(loop):
    # 创建webapp实例并绑定循环
    app = web.Application(loop=loop)
    # 注册处理函数到循环中
    app.router.add_route('GET','/',index)
    # app_runner = web.AppRunner(app)
    # 用协程创建监听服务
    srv = yield from loop.create_server(app._make_handler(),'127.0.0.1',9000)
    logging.info('start at http://127.0.0.1:9000...')
    return srv
# 创建事件循环
loop = asyncio.get_event_loop()
# 启动事件循环
loop.run_until_complete(init(loop))
# 持续运行
loop.run_forever()