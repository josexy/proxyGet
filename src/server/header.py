import random
class Header(object):
    def __init__(self):
        super().__init__()
        self.header_android_4_0_2 = "Mozilla/5.0 (Linux; U; Android 4.0.2; en-us; Galaxy Nexus Build/ICL53F) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30"
        self.header_android_2_3 = "Mozilla/5.0 (Linux; U; Android 2.3.6; en-us; Nexus S Build/GRK39F) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1"
        self.header_chrome_android = "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Mobile Safari/537.36"
        self.header_chrome_iphone = "Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1 (KHTML, like Gecko) CriOS/79.0.3945.88 Mobile/13B143 Safari/601.1.46"
        self.header_chrome_mac = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36"
        self.header_chrome_windows = "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36"
        self.header_chrome_linux = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36"

        self.header_fireforx_android = "Mozilla/5.0 (Android 4.4; Mobile; rv:46.0) Gecko/46.0 Firefox/46.0"
        self.header_fireforx_iphone = "Mozilla/5.0 (iPhone; CPU iPhone OS 8_3 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) FxiOS/1.0 Mobile/12F69 Safari/600.1.4"
        self.header_fireforx_mac = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:46.0) Gecko/20100101 Firefox/46.0"
        self.header_fireforx_windows = "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:46.0) Gecko/20100101 Firefox/46.0"

        self.header_IE11 = "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko"
        self.header_IE10 = "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)"
        self.header_IE9 = "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)"
        self.header_IE8 = "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)"

        self.header_microsoft_edge = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36 Edg/79.0.100.0"
        self.header_microsoft_edge_android = "Mozilla/5.0 (Linux; Android 8.1.0; Pixel Build/OPM4.171019.021.D1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.109 Mobile Safari/537.36 EdgA/42.0.0.2057"

        self.header_sofari_mac = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/7046A194A"
        self.header_sofari_ipad_ios_9 = "Mozilla/5.0 (iPad; CPU OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B137 Safari/601.1"

        self.header_uc_windows_phone = "Mozilla/5.0 (compatible; MSIE 10.0; Windows Phone 8.0; Trident/6.0; IEMobile/10.0; ARM; Touch; NOKIA; Lumia 920) UCBrowser/10.1.0.563 Mobile"
        self.header_uc_android = "Mozilla/5.0 (Linux; U; Android 8.1.0; en-US; Nexus 6P Build/OPM7.181205.001) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.108 UCBrowser/12.11.1.1197 Mobile Safari/537.36"
        self.header_uc_ios = "Mozilla/5.0 (iPhone; CPU iPhone OS 12_1 like Mac OS X; zh-CN) AppleWebKit/537.51.1 (KHTML, like Gecko) Mobile/16B92 UCBrowser/12.1.7.1109 Mobile AliApp(TUnionSDK/0.1.20.3)"
        self.ls_headers=[]

        self.ls_headers.append(self.header_android_4_0_2)
        self.ls_headers.append(self.header_android_2_3)
        self.ls_headers.append(self.header_chrome_android)
        self.ls_headers.append(self.header_chrome_iphone)
        self.ls_headers.append(self.header_chrome_linux)
        self.ls_headers.append(self.header_chrome_mac)
        self.ls_headers.append(self.header_chrome_windows)
        self.ls_headers.append(self.header_fireforx_android)
        self.ls_headers.append(self.header_fireforx_iphone)
        self.ls_headers.append(self.header_fireforx_mac)
        self.ls_headers.append(self.header_fireforx_windows)
        self.ls_headers.append(self.header_IE8)
        self.ls_headers.append(self.header_IE9)
        self.ls_headers.append(self.header_IE10)
        self.ls_headers.append(self.header_IE11)
        self.ls_headers.append(self.header_microsoft_edge)
        self.ls_headers.append(self.header_microsoft_edge_android)
        self.ls_headers.append(self.header_sofari_ipad_ios_9)
        self.ls_headers.append(self.header_sofari_mac)
        self.ls_headers.append(self.header_uc_android)
        self.ls_headers.append(self.header_uc_ios)
        self.ls_headers.append(self.header_uc_windows_phone)
    def random_header(self):
        return {'User-Agent':random.choice(self.ls_headers)}
    def __str__(self):
        return "User-Agent:{}".format(random.choice(self.ls_headers))
