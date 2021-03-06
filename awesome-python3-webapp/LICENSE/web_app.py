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

# 定义一个user类
from orm import Model, IntegertField, StringField
class user(Model):
    __table__ = 'users',
    id  = IntegertField(primary_key = True),
    name = StringField()
# 定义所有类的基类Model
class Model(dict, metaclass=ModelMetaclass):
    def __init__(self,**kw):
        super(Model,self).__init__(**kw)

    @classmethod
    @asyncio.coroutine
    def find(cls,pk):
        # 通过主键查找
        rs= yield from select('%s where "%s"=?' %(cls.__select__, cls.__primary_key__),[pk],1)
        if len(rs) == 0:
            return None
        return cls(**rs[0])
    @asyncio.coroutine
    def save(self):
        args = list(map(self.getValueOrDefault,self.__fields__))
        args.append(self.getValueOrDefault(self.__primary_key__))
        rows =yield from execute(self.__insert__,args)
        if rows !=1:
            logging.warn('failed to inserd record: affected rows: %s' %rows)
# 定义一个获取属性的方法
def __getattr__(self,key):
    try:
        return self[key]
    except KeyError:
        raise AttributeError(r"'Model' objecct has no attribute %s" %key)
# 定义一个设置属性的方法
def __setattr__(self,key,value):
    self[key] = value

# 定义一个获取值的方法
def getvalue(self,key):
    return __getattr__(self,key,None)

# 定义一个获取默认值并将其设置为值的方法
def getValueOrDefault(self ,key):
    value = getvalue(self,key,None)
    if value is None:
        field = self.__mappings__[key]
        if field.defaut is not None:
            value = field.default() if callable(field.default) else field.default
            logging.debug(r'using default value %s:%s' %(key,str(value)))
            setattr(self,key,value)
    return value

# 定义一个Field类
class Field(object):
    def __init__(self,name,column_type,primary_key,default):
        self.name = name,
        self.column_type = column_type,
        self.primary_key = primary_key,
        self.default = default

    def __str__(self):
        return '<%s,%s,%s>' % (self.__class__.__name__,self.column_type,self.name)

# 定义子类String并初始化varchar
class String(Field):
    def __init__(self,name=None,primary_key=False,default=None,ddl='varchar(100)'):
        super().__init__(name,ddl,primary_key,default)
# 定义元类Modelmataclass
class ModelMetaclass(type):
    def __new__(cls, name,bases,attrs):
        # 排除Model类本身
        if name == 'Model':
            return type.__new__(cls,name,bases,attrs)
        # 获取表名
        tableName = attrs.get('__table__',None) or name
        logging.info('found model:%s(table:%s)' %(name,tableName))
        # 获取所有的Field和主键名
        mappings = dict()
        Field = []
        primaryKey = None
        for k,v in attrs.item():
            if isinstance(v,Field):
                logging.info('found mapping: %s ==> %s' %(k,v))
                mappings[k] = v
                if v.primaryKey:
                    # 找到主键
                    if primaryKey:
                        raise RuntimeError('Duplicate primary key for field: %s' %k)
                    primaryKey = k
                else:
                    Field.append(k)
            if not primaryKey:
                raise RuntimeError('PrimaryKey is not found.')
            for k in mappings.keys():
                attrs.pop(k)
            escaped_fields = list(lambda f:'%s' % f,fields)
            attrs['__mappings__'] = mappings # 保存属性和列的映射关系
            attrs['__table__'] = tableName
            attrs['__primary_key__'] = primaryKey# 主键属性名
            attrs['__fields__'] = fields # 除主键外的属性名
            # 构造默认的SELECT, INSERT, UPDATE和DELETE语句:
            attrs['__select__'] = 'select `%s`, %s from `%s`' % (primaryKey, ', '.join(escaped_fields), tableName)
            attrs['__insert__'] = 'insert into `%s` (%s, `%s`) values (%s)' % (
            tableName, ', '.join(escaped_fields), primaryKey, create_args_string(len(escaped_fields) + 1))
            attrs['__update__'] = 'update `%s` set %s where `%s`=?' % (
            tableName, ', '.join(map(lambda f: '`%s`=?' % (mappings.get(f).name or f), fields)), primaryKey)
            attrs['__delete__'] = 'delete from `%s` where `%s`=?' % (tableName, primaryKey)
            return type.__new__(cls, name, bases, attrs)

