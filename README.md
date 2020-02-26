# proxyGet 0x1
proxyGet is a spider script which can sniff the website free proxies and store in the local database.

proxyGet爬取互联网上免费的代理IP存储在数据库中，而且proxyGet支持`同步`和`异步`方式来获取代理信息。

PS:代码仅供学习参考。

# proxyGet 0x2
src目录下文件
```bash
proxyChecker.py
proxyGet.py
proxyListenServer.py
proxyMessage.py
proxyOption.py
proxyPool.py
proxyReceiver.py
proxySQL.py
proxy_config.py
```
其中`proxyGet.py`是主要程序，可通过`./proxyGet.py --help`获取帮助信息

```bash
$ ./proxyGet.py -h

                                       ________        __   
    _____________  _______  ______.__./  _____/  _____/  |_ 
    \____ \_  __ \/  _ \  \/  <   |  /   \  ____/ __ \   __\ 
    |  |_> >  | \(  <_> >    < \___  \    \_\  \  ___/|  |  
    |   __/|__|   \____/__/\_ \/ ____|\______  /\___  >__|  
    |__|                     \/\/            \/     \/         
    
Usage: proxyGet.py [-0/1/2/3/4] [-5/6/7/8] [Opts] [SQL_Opt] [-h/-v/--author]

proxyGet is a spider script which can sniff the website free proxies and store
in the local database.

Options:
  -h, --help            show this help message and exit
  -v, --version         display the version info
  -m N, --max=N         maximum number of proxies [:20] all:-1
  -r CNT, --retry=CNT   the number of retries [:2]
  -t SEC, --timeout=SEC
                        the timeout for connecting to the url [:5]
  --author              display the author info
  --overwrite           overwrite if the database exists
  -a, --async           asynchronous fetch proxies
  --from=PAGE_INDEX     from page index [:1]
  --to=PAGE_INDEX       to page index [:1]

  Website type and support proxy type:
    -0                  the proxy type is Xila -5/6/7/8
    -1                  the proxy type is Nima -5/6/7/8
    -2                  the proxy type is Xici -5/6/7/8
    -3                  the proxy type is Kuai -5/6
    -4                  the proxy type is 7Yip -7

  Proxy type:
    -5                  common proxy type
    -6                  high anonymous proxy type
    -7                  http proxy type
    -8                  https proxy type

  Store in local databases or file,default sqlite3:
    --sqlite3           store the proxies in local  sqlite3 database
    --mysql             store the proxies in local or remote mysql database

  Extra SQL options:
    --host=HOST         specifies mysql local or remote host [:localhost]
    --port=PORT         specifies mysql local or remote port [:3306]
    --database=DB       specifies mysql database name [:db_proxy]
    -u U, --user=U      specifies mysql user
    -p P, --pwd=P       specifies mysql password
    -f FILE, --file=FILE
                        specifies sqlite3 database file path [:db/test.db]
    --table=TB          specifies mysql or sqlite3 table name [:tb_proxy
```
# proxyGet 0x3
`proxyListenServer.py`通过`Flask`框架搭建一个简单的代理接口，默认URL为`http://localhost:5000`，而`proxyReceiver.py`能够在获取完成代理信息后进一步进行检测是否可行，若不可行则并从数据库中删除，从而维护代理池。`proxy_config.py`作为配置文件管理`proxyListenServer.py`和`proxyReceiver.py`。

# proxyGet 0x4
支持存储代理信息的数据库，功能很简单：
- SQLite
- MySQL

# proxyGet 0x5
proxyGet能够在Windows和Linux上运行。
首先安装相应的库
```bash
pip install -r requirements.txt
```
例子：
```python
proxyGet.py -0 -5
proxyGet.py -3 -7 --async
proxyGet.py -0 -7 -m 10 -t 5 --mysql --host=127.0.0.1 --port=3306 -u root -p xxx --database=db_proxy --table=tb_proxy
proxyGet.py -1 -5 --async --max=2 --timeout=3 --retry=1 --file=db/test.db --table=tb_proxy --from=2 --to=4
proxyGet.py -1 -5 --async --max=2 --timeout=3 --retry=1 --file=c:/db/test.db --table=tb_proxy --from=2 --to=4
proxyGet.py -2 -6 --max=-1 -f c:\db\test.db --table=tb_proxy --from=2 --to=4
```
