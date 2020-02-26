
import re
import signal
import requests
import asyncio
import aiohttp
from queue import Queue
from pyquery import PyQuery
from server.header import Header
from proxySQL import proxySQLite,proxyMySQL
from server.collectProxyList import ProxyIpInfo
from proxyMessage import CliMessage,Color

"""代理池"""
class BaseTestProxyPool(object):
    """
    Base TestProxyPool class
    """
    def __init__(self,table_field=None,optBox=None):
        super().__init__()
        self.optBox=optBox
        self.table_field=table_field
        self.cur_size=0
        self.max_size=self.optBox['max_proxies']
        if self.max_size<=0:
            self.max_size=0
        self.retry=self.optBox['retry']
        self.overwrite=self.optBox['overwrite']
        self.q_ips=Queue(self.max_size)

        # request session
        self.session=None
        self.headers = Header().random_header()
        self.timeout=self.optBox['timeout']
        self._async=self.optBox['_async']
        self.verify=False
        self.test_url='http://httpbin.org'

        # sql database type
        if self.optBox['mysql']:
            self.sqlConn=proxyMySQL(
                host=self.optBox['mysql_host'],
                port=self.optBox['mysql_port'],
                user=self.optBox['mysql_user'],
                pwd=self.optBox['mysql_pwd'],
                database_name=self.optBox['mysql_db'],
                table_name=self.optBox['mysql_sqlite_tb'],
                table_field=self.table_field,
                overwrite=self.overwrite
            )
            self.sqlConn.create_database()
            self.sqlConn.create_table()
        else:
            # self.optBox['sqlite3'] => default
            self.sqlConn=proxySQLite(
                database_path=self.optBox['sqlite_file_path'],
                table_name=self.optBox['mysql_sqlite_tb'],
                table_field=self.table_field,
                overwrite=self.overwrite
            )
            self.sqlConn.create_table()
    def signal_callback(self,*args):
        """
        reveice SIGINT signal and exit
        """
        self.q_ips.task_done()
        self.q_ips.queue.clear()
        if hasattr(self,'sqlConn'):
            if self.sqlConn:
                del self.sqlConn
        if self._async:
            try:
                self.loop.stop()
                self.loop.close()
            except:
                pass
        CliMessage.print_with_status('Exit...',Color.Red,Color.Bold,None,'failed')
        exit(0)
    def add_ip(self,ip):
        """
        Add proxy ip until the Queue is filled
        :param ip: => ProxyIpInfo or dict
        """
        if not isinstance(ip,ProxyIpInfo) and not isinstance(ip,dict):
            return False
        if self.max_size > 0:
            if self.cur_size >= self.max_size:
                return False
        if isinstance(ip,dict):
            ip=ProxyIpInfo(ip)
        self.q_ips.put(ip)
        self.cur_size+=1
        return True
    def test_ip(self,ip_proxy=None,verify=False,test_url=None):
        pass
    def start_test(self):
        pass
    def __get(self,ip_proxy):
        """
        Gets the real IP ownership proxy location
        """
        try:
            url = 'https://ip.cn/?ip=' + ip_proxy.split(':')[0]
            with requests.session().get(url=url, headers=self.headers, timeout=self.timeout) as resp:
                text = resp.text
                rgx = re.compile(r'<code>(.*?)</code>', re.IGNORECASE | re.MULTILINE)
                self.ip_result = re.findall(rgx, text)
        except:
            self.ip_result = None
    def get_current_proxyip_info(self,ip_proxy):
        self.__get(ip_proxy)
        return self.ip_result
class TestProxyPool(BaseTestProxyPool):
    def __init__(self,table_field=None,optBox=None):
        super().__init__(table_field,optBox)
        self.session=requests.session()
        signal.signal(signal.SIGINT,self.signal_callback)
    def __del__(self):
        if hasattr(self,'sqlConn') and self.sqlConn:
            del self.sqlConn
        self.session.close()
    def test_ip(self,ip_proxy=None):
        status_code=0
        try:
            with self.session.get(url=self.test_url,proxies=ip_proxy,
                                timeout=self.timeout,verify=self.verify,
                                headers=self.headers) as r:
                status_code = r.status_code
        except:
            status_code=0
        return status_code
    def start_test(self):
        while not self.q_ips.empty():
            proxyIPinfo=self.q_ips.get()
            per_proxies = proxyIPinfo.proxies
            if self.sqlConn.find_exist(per_proxies):
                continue
            proxies = {
                'http': 'http://'+per_proxies,
                'https': 'http://' + per_proxies
            }
            CliMessage.print_with_status(f'Testing {per_proxies}', Color.Green)
            _retry=self.retry
            while _retry > 0:
                # Test IP
                ls_ip_info=self.test_ip(proxies)
                if ls_ip_info==200:
                    CliMessage.print_with_status(f'OK!', Color.Green,Color.Bold)
                    ls=proxyIPinfo.values()
                    real_ip_info=self.get_current_proxyip_info(per_proxies)
                    if not self.sqlConn.find_exist(per_proxies):
                        if real_ip_info and isinstance(real_ip_info,list):
                            ls[1]=real_ip_info[1]+real_ip_info[2]
                            self.sqlConn.insert(ls)
                        else:
                            self.sqlConn.insert(ls)
                        break
                else:
                    CliMessage.print_with_status(f'Retrying...', Color.Yellow, None,None,'warning')
                    _retry-=1
        self.cur_size=0
class asyncTestProxyPool(BaseTestProxyPool):
    def __init__(self,table_field=None,optBox=None):
        super().__init__(table_field,optBox)
    def __del__(self):
        if hasattr(self,'sqlConn') and self.sqlConn:
            del self.sqlConn
    async def test_ip(self,ip_proxy=None):
        statue_code=0
        try:
            timeout=aiohttp.ClientTimeout(self.timeout)
            async with aiohttp.ClientSession(headers=self.headers,timeout=timeout) as session:
                async with session.get(url=self.test_url,proxy=ip_proxy,verify_ssl=self.verify) as r:
                    statue_code=r.status
        except:
            statue_code=0
        return statue_code
    async def _async_start_test(self):
        while not self.q_ips.empty():
            proxyIPinfo=self.q_ips.get()
            per_proxies = proxyIPinfo.proxies
            if self.sqlConn.find_exist(per_proxies):
                continue
            proxies = 'http://'+per_proxies
            CliMessage.print_with_status(f'Testing {per_proxies}', Color.Green)
            _retry=self.retry
            while _retry > 0:
                # deal with next IP
                ls_ip_info=await self.test_ip(proxies)
                if ls_ip_info==200:
                    CliMessage.print_with_status(f'OK! {per_proxies}', Color.Green,Color.Bold)
                    ls=proxyIPinfo.values()
                    real_ip_info=self.get_current_proxyip_info(per_proxies)
                    if real_ip_info and len(real_ip_info)>=3 and ls and len(ls)>=2:
                        ls[1]=real_ip_info[1]+real_ip_info[2]
                        self.sqlConn.insert(ls)
                    else:
                        self.sqlConn.insert(ls)
                    break
                else:
                    CliMessage.print_with_status(f'Retrying {per_proxies}', Color.Yellow, None,None,'warning')
                    _retry-=1
    def start_test(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        task_proxies=[]
        for i in range(self.max_size):
            task_proxies.append(self._async_start_test())
        self.loop.run_until_complete(asyncio.wait(task_proxies))
        self.cur_size=0
        self.q_ips.queue.clear()
