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

# 创建一个连接池
import aiomysql
@asyncio.coroutine
def create_pool(loop,**kw):
    logging.info('start creats databases connection pool...')
    # 定义一个全局参数
    global _pool
    # 使用kw传入的参数创建一个连接池，方便复用
    _pool = yield from aiomysql.create(
        host = kw.get('host','localhost'),
        port = kw.get('port','3320'),
        user = kw['user'],
        password = kw['password'],
        db = kw['db'],
        charset = kw.get('charset','utf8'),
        autocommit = kw.get('autocommit',True),
        maxsize = kw.get('maxsize','10'),
        minsize = kw.get('minsize','1'),
        loop = loop
    )

# 封装select函数
@asyncio.coroutine
def select(sql,args,size = None):
    logging.info(sql,args)
    global _pool
    with (yield from _pool) as cnn:
        # 创建协程游标
        cur  = yield from cnn.cursor(aiomysql.DictCursor) #查询的返回格式会变成字典格式
        yield from cur.execute(sql.replace('?',"%s"), args or ())#替换为sql中的占位符
        if size:
            rs = yield from cur.fetchmany(size)
        else:
            rs = yield from cur.fetchall()
            # 如果传入size参数，就通过fetchmany()获取最多指定数量的记录，否则，通过fetchall()获取所有记录。
        yield from cur.close()
        logging.info('rows returned:%s' % len(rs))
        return rs
# 封装insert/update/delete函数
@asyncio.coroutine
def execute(sql,args):
    logging.info(sql)
    with (yield from _pool) as cnn:
        try:
            cur = yield from cnn.cursor()
            yield from cur.execute(sql.replace('?','%s'),args)
            affected  = cur.rowcount
            yield from cur.closed()
        except BaseException as e:
            raise
        return affected
