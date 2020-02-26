
# 本地监听IP 地址
LISTEN_HOST='localhost'
# 端口
LISTEN_PORT=5000
# 是否调试
DEBUG=False

# os.urandom(16).hex()
SECRET_KEY='fcc7776ad81d074865e010211587857b'

# proxyReceiver and proxyListenServer configuration
# 以下配置主要作用于 proxyReceiver.py 和 proxyListenServer.py
# 设置SQL类型
# SQL_TYPE='mysql'
SQL_TYPE='sqlite'
# 是否在终端显示输出信息
OUTPUT_DEBUG_INFO=True
# SQLite数据库文件
DATABASE_PATH='db/test.db'
# MySQL 本地/远程主机
MYSQL_HOST='localhost'
# MySQL 本地/远程主机端口
MYSQL_PORT=3306
# MySQL 用户名
MYSQL_USER='root'
# MySQL 密码
MYSQL_PWD='root'
# MySQL 数据库
DATABASE='db_proxy'
# SQLite 和 MySQL 表
TABLE='tb_proxy'
# 是否重新写入数据库,之前的内容全部清除
OVERWRITE=False
# 最大测试代理条数
MAX_PROXIES=20
# 测试连接超时时间
TIMEOUT=5
# 测试连接失败时重试次数
RETRY=2
