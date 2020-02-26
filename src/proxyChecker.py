#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

import time
import asyncio
import aiohttp
import proxy_config
from proxySQL import proxySQLite,proxyMySQL
from proxyMessage import CliMessage,Color
from optparse import OptionParser

class ProxyChecker(object):
    def __init__(self,sqlConn=None,url='http://httpbin.org',headers=None,timeout=6,verify=False):
        super().__init__()
        if not isinstance(sqlConn,proxySQLite) and not isinstance(sqlConn,proxyMySQL):
            raise TypeError("sqlConn type not proxyMySQL or proxySQLite!")
        self.sqlConn=sqlConn
        self.url=url
        self.headers=headers
        self.timeout=timeout
        self.verify=verify
        self.index=0
        self.failed_count=0
        self.successed_count=0
    async def __check(self,proxy,delete_invalid_proxies):
        for p in range(2):
            try:
                async with aiohttp.ClientSession(headers=self.headers) as session:
                    async with session.get(self.url, timeout=self.timeout, proxy='http://'+proxy,verify_ssl=self.verify) as resp:
                        self.status_code = resp.status
                        break
            except:
                self.status_code=0
        if self.status_code==200:
            self.index+=1
            self.successed_count+=1
            CliMessage.print_with_status(f'Good.{self.index} http://{proxy}',Color.Green)
        else:
            self.failed_count+=1
            if delete_invalid_proxies:
                if not self.sqlConn.is_closed():
                    self.sqlConn.remove(value=proxy)
    def done(self,task):
        CliMessage.print_with_status('Done',Color.Green,Color.Bold)
        CliMessage.print_with_status(f'Successful prixies: {self.successed_count}',Color.Green,Color.Bold)
        CliMessage.print_with_status(f'Failed prixies: {self.failed_count}',Color.Red,Color.Bold,status='failed')

    async def start_check(self,loop,delete_invalid_proxies=True):
        tasks = []
        for i in self.sqlConn.fetch_one_row():
            if i is not None:
                tasks.append(self.__check(i[1], delete_invalid_proxies))
        if len(tasks) <= 0:
            CliMessage.print_with_status('No tasks to check!', Color.Yellow, status='warning')
            return
        await asyncio.gather(*tasks)

def main():
    parser = OptionParser('proxyChecker -h/-d/-r')
    parser.set_description('proxyChecker check the proxies and remove invalid proxies from database.')
    parser.add_option('-t', action='store', metavar='SEC', default=6, dest='timeout', help='connection timeout [:6]',
                      type='int')
    parser.add_option('-d', action='store_true', dest='delete', help='delete invalid proxies')
    parser.add_option('-r', action='store_true', dest='run_forever', help='run forever but wait for 5 seconds')
    (opt, args) = parser.parse_args()


    if proxy_config.SQL_TYPE == 'sqlite':
        sqlConn = proxySQLite(proxy_config.DATABASE_PATH, proxy_config.TABLE)
    else:
        sqlConn = proxyMySQL(proxy_config.MYSQL_USER, proxy_config.MYSQL_PWD,
                             host=proxy_config.MYSQL_HOST, port=proxy_config.MYSQL_PORT,
                             database_name=proxy_config.DATABASE, table_name=proxy_config.TABLE)
    delete_invalid_proxies = False
    if opt.delete:
        CliMessage.print_with_status("proxyChecker will delete invalid proxies!", Color.Yellow, status='warning')
        delete_invalid_proxies = True

    loop = asyncio.get_event_loop()
    # run forever
    while True:
        checker = ProxyChecker(sqlConn, timeout=opt.timeout)
        try:
            gather = asyncio.gather(checker.start_check(loop, delete_invalid_proxies))
            gather.add_done_callback(checker.done)
            loop.run_until_complete(gather)
        except KeyboardInterrupt:
            CliMessage.print_with_status('Exit......', Color.Red, Color.Bold, status='failed')
            if sqlConn.is_closed():
                loop.close()
            exit(0)
        finally:
            # database was closed
            if sqlConn.is_closed():
                CliMessage.print_with_status('Database was closed!', Color.Red, Color.Bold, status='failed')
                loop.close()
                exit(0)
        if not opt.run_forever:
            break
        time.sleep(5)
    loop.close()
    sqlConn.close()

if __name__=='__main__':
    main()