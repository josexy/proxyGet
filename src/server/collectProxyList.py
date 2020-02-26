
import requests
from lxml import etree
from pyquery import PyQuery
from server import proxyServer
from server.header import Header

class ProxyIpInfo(object):
    def __init__(self,one_proxy_ip):
        """
        one_proxy_ip: dict{...}
        """
        super().__init__()
        self.ip = dict(one_proxy_ip)
        self.lp=[]
        self.lp.append(self.ip.get('proxies',None))
        self.lp.append(self.ip.get('location',None))
    @property
    def proxies(self):
        return self.ip.get('proxies',None)
    @property
    def location(self):
        return self.ip.get('location',None)
    def values(self):
        return [x for x in self.lp if x]

"""获取代理网站相应代理信息"""
class ProxyBaseControl(object):
    def __init__(self,url,page_index=1):
        super().__init__()
        self.url=url
        self.page_index=page_index
        self.html=""
    def set_page_index(self,page_index):
        self.page_index=page_index
    def __get_htmlcode(self):
        pass
    def run(self):
        pass
    def table_field(self):
        return ['proxies','location']
class Xila(ProxyBaseControl):
    def __init__(self,url,page_index=1):
        super().__init__(url,page_index)
    def __get_htmlcode(self):
        url=self.url+"/"+str(self.page_index)
        try:
            with requests.session().request("get", url, headers=Header().random_header()) as resp:
                self.html = resp.text
        except:
            self.html=None
    def run(self):
        self.__get_htmlcode()
        if not self.html:
            raise StopIteration()
        doc=PyQuery(self.html)
        for p in doc(".fl-table tbody tr").items():
            one={}
            one['proxies']=p.children().eq(0).text()
            one['location']=p.children().eq(3).text()
            yield one
class Nima(Xila):
    def __init__(self,url,page_index=1):
        super().__init__(url,page_index)
class Yip7(ProxyBaseControl):
    def __init__(self,url,page_index=1):
        super().__init__(url,page_index)
    def __get_htmlcode(self):
        url=self.url+"/?action=china&page="+str(self.page_index)
        try:
            with requests.session().request("get", url, headers=Header().random_header()) as resp:
                self.html = resp.text
        except:
            self.html=None
    def run(self):
        self.__get_htmlcode()
        if not self.html:
            raise StopIteration()
        doc = PyQuery(self.html)
        for p in doc('tbody tr').items():
            html = etree.HTML(str(p))
            record=html.xpath("//tr/td/text()")
            one={}
            one['proxies']=record[0]+':'+record[1]
            one['location']=record[4]
            yield one
class Kuai(ProxyBaseControl):
    def __init__(self,url,page_index=1):
        super().__init__(url,page_index)
    def __get_htmlcode(self):
        url=self.url+"/"+str(self.page_index)
        try:
            with requests.session().request("get", url, headers=Header().random_header()) as resp:
                self.html = resp.text
        except:
            self.html=None
    def run(self):
        self.__get_htmlcode()
        if not self.html:
            raise StopIteration()
        doc=PyQuery(self.html)
        for p in doc("table tbody tr").items():
            one={}
            one['proxies']=f"{p.children().eq(0).text()}:{p.children().eq(1).text()}"
            one['location']=p.children().eq(4).text()
            yield one
class Xici(Xila):
    def __init__(self,url,page_index=1):
        super().__init__(url,page_index)
    def __get_htmlcode(self):
        url=self.url+'/'+str(self.page_index)
        try:
            with requests.session().request("get", url, headers=Header().random_header()) as resp:
                self.html = resp.text
        except:
            self.html=None
    def run(self):
        self.__get_htmlcode()
        if not self.html:
            raise StopIteration()
        doc=PyQuery(self.html)
        for p in doc('tr.odd').items():
            one={}
            one['proxies']=f"{p.children().eq(1).text()}:{p.children().eq(2).text()}"
            one['location']=p.children().eq(3).text()
            yield one

