
class ProxyServerBase(object):
    def __init__(self,url=None):
        super().__init__()
        self._url=url
    def url():
        return self._url
    def __str__(self):
        return self._url
    def proxy_types(self):
        return ['common','high_anonymous','http','https']

class XilaProxy(ProxyServerBase):
    def __init__(self,url='http://www.xiladaili.com'):
        super().__init__(url=url)
    def commmon_proxy(self):
        return self._url+"/putong"
    def high_anonymous_proxy(self):
        return self._url+"/gaoni"
    def http_proxy(self):
        return self._url+"/http"
    def https_proxy(self):
        return self._url+"/https"

class NimaProxy(ProxyServerBase):
    def __init__(self, url='http://www.nimadaili.com'):
        super().__init__(url=url)
    def commmon_proxy(self):
        return self._url+"/putong"
    def high_anonymous_proxy(self):
        return self._url+"/gaoni"
    def http_proxy(self):
        return self._url+"/http"
    def https_proxy(self):
        return self._url+"/https"

class XiciProxy(ProxyServerBase):
    def __init__(self, url='https://www.xicidaili.com'):
        super().__init__(url=url)
    def commmon_proxy(self):
        return self._url+"/nt"
    def high_anonymous_proxy(self):
        return self._url+"/nn"
    def http_proxy(self):
        return self._url+"/wt"
    def https_proxy(self):
        return self._url+"/wn"

class KuaiProxy(ProxyServerBase):
    def __init__(self, url='https://www.kuaidaili.com'):
        super().__init__(url=url)
    def commmon_proxy(self):
        return self._url+"/free/intr"
    def high_anonymous_proxy(self):
        return self._url+"/free/inha"
    def proxy_types(self):
        return ['common','high_anonymous']

class Yip7Proxy(ProxyServerBase):
    def __init__(self, url='https://www.7yip.cn'):
        super().__init__(url=url)
    def http_proxy(self):
        return self._url+'/free'
    def proxy_types(self):
        return ['http']
