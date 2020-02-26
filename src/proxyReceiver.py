#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

import random
import asyncio
import proxy_config
from proxyPool import asyncTestProxyPool
from server import collectProxyList,proxyServer
from proxyMessage import CliMessage,Color

def _async_start_sniff(col,opt):
    test_pool=asyncTestProxyPool(col.table_field(),opt)
    for ip in col.run():
        if not test_pool.add_ip(ip):
            break
    try:
        test_pool.start_test()
    except:
        exit(-1)
def main():
    optBox={}
    optBox['max_proxies']=proxy_config.MAX_PROXIES
    optBox['retry']=proxy_config.RETRY
    optBox['timeout']=proxy_config.TIMEOUT
    optBox['overwrite']=proxy_config.OVERWRITE
    optBox['mysql_host']=proxy_config.MYSQL_HOST
    optBox['mysql_port']=proxy_config.MYSQL_PORT
    optBox['mysql_user']=proxy_config.MYSQL_USER
    optBox['mysql_pwd']=proxy_config.MYSQL_PWD
    optBox['mysql_db']=proxy_config.DATABASE
    optBox['mysql_sqlite_tb']=proxy_config.TABLE
    optBox['sqlite_file_path']=proxy_config.DATABASE_PATH
    if proxy_config.SQL_TYPE=='mysql':
        optBox['mysql'] = True
        optBox['sqlite3'] = False
    else:
        optBox['mysql'] = False
        optBox['sqlite3'] = True
    optBox['_async'] = True

    urls_xila=[
        proxyServer.XilaProxy().commmon_proxy(),
        proxyServer.XilaProxy().high_anonymous_proxy(),
        proxyServer.XilaProxy().http_proxy(),
        proxyServer.XilaProxy().https_proxy()
    ]
    urls_nima=[
        proxyServer.NimaProxy().commmon_proxy(),
        proxyServer.NimaProxy().high_anonymous_proxy(),
        proxyServer.NimaProxy().http_proxy(),
        proxyServer.NimaProxy().https_proxy()
    ]
    urls_xici=[
        proxyServer.XiciProxy().commmon_proxy(),
        proxyServer.XiciProxy().high_anonymous_proxy(),
        proxyServer.XiciProxy().http_proxy(),
        proxyServer.XiciProxy().https_proxy()
    ]
    urls_kuai=[
        proxyServer.KuaiProxy().commmon_proxy(),
        proxyServer.KuaiProxy().high_anonymous_proxy()
    ]

    collects=[
        collectProxyList.Xila(random.choice(urls_xila)),
        collectProxyList.Nima(random.choice(urls_nima)),
        collectProxyList.Yip7(proxyServer.Yip7Proxy().http_proxy()),
        collectProxyList.Xici(random.choice(urls_xici)),
        collectProxyList.Kuai(random.choice(urls_kuai))
    ]
    cols=collects
    while True:
        for i in cols:
            _async_start_sniff(i, optBox)
        cols = collects
if __name__=='__main__':
    main()
