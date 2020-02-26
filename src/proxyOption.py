
from server import Logo
from proxyMessage import CliMessage,Color
from server import proxyServer,collectProxyList
from optparse import OptionParser,OptionGroup

class OptionBox(object):
    def __init__(self):
        super().__init__()
        self.options={}
    def add_key_value(self,key,value):
        if key and value:
            self.options[key]=value
    def get_value(self,key):
        # safe
        return self.options.get(key,None)
    def __getitem__(self, key):
        # safe
        return self.options.get(key,None)
    def __str__(self):
        return str(self.options)

class HelpPanel(object):
    def __init__(self):
        self.version="1.0.0"
        self.author='Joseph.XRays'
        self.blog='https://www.joxrays.com'

        super().__init__()
        self.output_logo()
        self.__optparser=OptionParser()
        self.set_usage()
        self.set_description()
        self.initialized_panel()
        self.__optBox=OptionBox()
        self.parser_options()

    def __getitem__(self, option):
        return self.__optBox.get_value(option)

    def set_description(self):
        self.__optparser.set_description('proxyGet is a spider script which can sniff the website free proxies and store in the local database.')
    def set_usage(self):
        self.__optparser.set_usage('proxyGet.py [-0/1/2/3/4] [-5/6/7/8] [Opts] [SQL_Opt] [-h/-v/--author]')

    def initialized_panel(self):
        self.__optparser.add_option('-v','--version',action='store_true',dest='version',help='display the version info')
        self.__optparser.add_option('-m','--max',action='store',metavar='N',dest='max_proxies',default=20,help='maximum number of proxies [:20] all:-1',type='int')
        self.__optparser.add_option('-r','--retry',action='store',metavar='CNT',dest='retry',default=2,help='the number of retries [:2]',type='int')
        self.__optparser.add_option('-t','--timeout',action='store',metavar='SEC',dest='timeout',default=5,help='the timeout for connecting to the url [:5]',type='int')
        self.__optparser.add_option('--author',action='store_true',dest='author',help='display the author info')
        self.__optparser.add_option('--overwrite',action='store_true',dest='overwrite',help='overwrite if the database exists')
        self.__optparser.add_option('-a','--async',action='store_true',dest='_async',help='asynchronous fetch proxies')
        self.__optparser.add_option('--from',action='store',metavar='PAGE_INDEX',dest='from_page_index',default=1,help='from page index [:1]',type='int')
        self.__optparser.add_option('--to',action='store',metavar='PAGE_INDEX',dest='to_page_index',default=1,help='to page index [:1]',type='int')

        self.__group_store_way=OptionGroup(self.__optparser,'Store in local databases or file,default sqlite3')
        self.__group_store_way.add_option('--sqlite3',dest='sqlite3',action='store_true',help='store the proxies in local  sqlite3 database')
        self.__group_store_way.add_option('--mysql',dest='mysql',action='store_true',help='store the proxies in local or remote mysql database')

        self.__extra_option=OptionGroup(self.__optparser,'Extra SQL options')
        # mysql option info
        self.__extra_option.add_option('--host',metavar='HOST',dest='mysql_host',default='localhost',help='specifies mysql local or remote host [:localhost]',action='store',type='string')
        self.__extra_option.add_option('--port',metavar='PORT',dest='mysql_port',default=3306,help='specifies mysql local or remote port [:3306]',action='store',type='int')
        self.__extra_option.add_option('--database',metavar='DB',dest='mysql_db',default='db_proxy',help='specifies mysql database name [:db_proxy]',action='store',type='string')
        self.__extra_option.add_option('-u','--user',metavar='U',dest='mysql_user',help='specifies mysql user',action='store',type='string')
        self.__extra_option.add_option('-p','--pwd',metavar='P',dest='mysql_pwd',help='specifies mysql password',action='store',type='string')
        # sqlite option info
        self.__extra_option.add_option('-f','--file',metavar='FILE',dest='sqlite_file_path',default='db/test.db',help='specifies sqlite3 database file path [:db/test.db]',action='store',type='string')
        # common option info
        self.__extra_option.add_option('--table',metavar='TB',dest='mysql_sqlite_tb',default='tb_proxy',help='specifies mysql or sqlite3 table name [:tb_proxy]',action='store',type='string')

        # different free proxy websites
        self.__website_type=OptionGroup(self.__optparser,'Website type and support proxy type')
        self.__website_type.add_option('-0',action='store_true',dest='proxy_type_xila',help='the proxy type is Xila -5/6/7/8')
        self.__website_type.add_option('-1',action='store_true',dest='proxy_type_nima',help='the proxy type is Nima -5/6/7/8')
        self.__website_type.add_option('-2',action='store_true',dest='proxy_type_xici',help='the proxy type is Xici -5/6/7/8')
        self.__website_type.add_option('-3',action='store_true',dest='proxy_type_kuai',help='the proxy type is Kuai -5/6')
        self.__website_type.add_option('-4',action='store_true',dest='proxy_type_yip7',help='the proxy type is 7Yip -7')

        # proxy type
        self.__proxy_subtype = OptionGroup(self.__optparser, 'Proxy type')
        self.__proxy_subtype.add_option('-5',action='store_true',dest='proxy_common',help='common proxy type')
        self.__proxy_subtype.add_option('-6',action='store_true',dest='proxy_high_anonymous',help='high anonymous proxy type')
        self.__proxy_subtype.add_option('-7',action='store_true',dest='proxy_http',help='http proxy type')
        self.__proxy_subtype.add_option('-8',action='store_true',dest='proxy_https',help='https proxy type')

        self.__optparser.add_option_group(self.__website_type)
        self.__optparser.add_option_group(self.__proxy_subtype)
        self.__optparser.add_option_group(self.__group_store_way)
        self.__optparser.add_option_group(self.__extra_option)
        (opt,args)=self.__optparser.parse_args()
        self.__opt=opt

    def parser_options(self):
        self.__optBox.add_key_value('proxy_type_xila',self.__opt.proxy_type_xila)
        self.__optBox.add_key_value('proxy_type_nima',self.__opt.proxy_type_nima)
        self.__optBox.add_key_value('proxy_type_xici',self.__opt.proxy_type_xici)
        self.__optBox.add_key_value('proxy_type_kuai',self.__opt.proxy_type_kuai)
        self.__optBox.add_key_value('proxy_type_yip7',self.__opt.proxy_type_yip7)

        self.__optBox.add_key_value('proxy_common',self.__opt.proxy_common)
        self.__optBox.add_key_value('proxy_high_anonymous',self.__opt.proxy_high_anonymous)
        self.__optBox.add_key_value('proxy_http',self.__opt.proxy_http)
        self.__optBox.add_key_value('proxy_https',self.__opt.proxy_https)

        self.__optBox.add_key_value('max_proxies',self.__opt.max_proxies)
        self.__optBox.add_key_value('retry',self.__opt.retry)
        self.__optBox.add_key_value('timeout',self.__opt.timeout)
        self.__optBox.add_key_value('author',self.__opt.author)
        self.__optBox.add_key_value('version',self.__opt.version)
        self.__optBox.add_key_value('overwrite',self.__opt.overwrite)
        self.__optBox.add_key_value('from_page_index',self.__opt.from_page_index)
        self.__optBox.add_key_value('to_page_index',self.__opt.to_page_index)
        self.__optBox.add_key_value('_async',self.__opt._async)

        self.__optBox.add_key_value('sqlite3',self.__opt.sqlite3)
        self.__optBox.add_key_value('mysql',self.__opt.mysql)

        self.__optBox.add_key_value('mysql_host',self.__opt.mysql_host)
        self.__optBox.add_key_value('mysql_port',self.__opt.mysql_port)
        self.__optBox.add_key_value('mysql_user',self.__opt.mysql_user)
        self.__optBox.add_key_value('mysql_pwd',self.__opt.mysql_pwd)
        self.__optBox.add_key_value('mysql_db',self.__opt.mysql_db)
        self.__optBox.add_key_value('mysql_sqlite_tb',self.__opt.mysql_sqlite_tb)
        self.__optBox.add_key_value('sqlite_file_path',self.__opt.sqlite_file_path)

        if self.__optBox['author']:
            self.display_author_info()
            exit(0)
        if self.__optBox['version']:
            CliMessage.print_with_status(f"proxyGet version: v{self.version}")
            exit(0)

        if self.__optBox['proxy_type_xila']:
            self.interface = proxyServer.XilaProxy
            self.collect = collectProxyList.Xila
        elif self.__optBox['proxy_type_nima']:
            self.interface = proxyServer.NimaProxy
            self.collect = collectProxyList.Nima
        elif self.__optBox['proxy_type_xici']:
            self.interface = proxyServer.XiciProxy
            self.collect = collectProxyList.Xici
        elif self.__optBox['proxy_type_kuai']:
            self.interface = proxyServer.KuaiProxy
            self.collect = collectProxyList.Kuai
        elif self.__optBox['proxy_type_yip7']:
            self.interface = proxyServer.Yip7Proxy
            self.collect = collectProxyList.Yip7
        else:
            CliMessage.print_with_status('please choose a website type!', Color.Red, None, None, 'failed')
            exit(-1)
        if self.interface != proxyServer.Yip7Proxy and self.interface != proxyServer.KuaiProxy:
            if self.__optBox['proxy_common']:
                self.url = self.interface().commmon_proxy()
            elif self.__optBox['proxy_high_anonymous']:
                self.url = self.interface().high_anonymous_proxy()
            elif self.__optBox['proxy_http']:
                self.url = self.interface().http_proxy()
            elif self.__optBox['proxy_https']:
                self.url = self.interface().https_proxy()
            else:
                CliMessage.print_with_status('please choose a proxy type!',Color.Red,None,None,'failed')
                exit(-1)
        elif self.interface==proxyServer.KuaiProxy:
            if self.__optBox['proxy_common']:
                self.url = self.interface().commmon_proxy()
            elif self.__optBox['proxy_high_anonymous']:
                self.url = self.interface().high_anonymous_proxy()
            else:
                CliMessage.print_with_status('please choose a proxy type!', Color.Red, None, None, 'failed')
                exit(-1)
        else:
            if self.__optBox['proxy_http']:
                self.url = self.interface().http_proxy()
            else:
                CliMessage.print_with_status('please choose a proxy type!',Color.Red,None,None,'failed')
                exit(-1)
    def display_author_info(self):
        CliMessage.print_with_status(f'Author: {self.author}',Color.Cyan)
        CliMessage.print_with_status(f'Blog: {self.blog}',Color.Green)
    def output_logo(self):
        CliMessage.print(Logo.text(),Color.random_fgcolor(),Color.Bold)
    @property
    def optionBox(self):
        return self.__optBox
