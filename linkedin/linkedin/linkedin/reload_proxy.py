# -*- coding: utf-8 -*-
import os
import re
import time
import datetime
from urllib2 import URLError, HTTPError
import sys
import urllib2

######################################
# Loader
######################################
class ProxyResource:
    def __init__(self):
        self.html_getter = WebPageDownloader();
        # self.filename = os.path.join(self.settings.resourcedir, "proxies.txt")

    def load_proxycn(self):
        '''
        '''
        # class resource
        psource_template = "http://www.proxycn.cn/html_proxy/port%s-%s.html"
        psource_ports = (8080, 80, 81, 3128, 8000, 1080, 444)
        p_nextpage = re.compile("<a href=[^>]*>下一页</a>")
        p_proxy = re.compile("<TR [^>]* onDblClick=\"clip\\('([\\d.]+):(\\d+)'\\);alert\\('已拷贝到剪贴板!'\\)[^\\x00]+?<TD class=\"list\">\\d+</TD><TD class=\"list\">(\\w*)</TD><TD class=\"list\">([^<]*)</TD><TD class=\"list\">([^<]*)</TD>")

        # another place
        proxy_urls = []
        proxy_urls.append("http://www.cnproxy.com/proxy1.html");
        proxy_urls.append("http://www.cnproxy.com/proxy2.html");
        proxy_urls.append("http://www.cnproxy.com/proxy3.html");
        proxy_urls.append("http://www.cnproxy.com/proxy4.html");
        proxy_urls.append("http://www.cnproxy.com/proxy5.html");
        proxy_urls.append("http://www.cnproxy.com/proxy6.html");
        proxy_urls.append("http://www.cnproxy.com/proxy7.html");
        proxy_urls.append("http://www.cnproxy.com/proxy8.html");
        proxy_urls.append("http://www.cnproxy.com/proxy9.html");
        proxy_urls.append("http://www.cnproxy.com/proxy10.html");
        p_proxy2 = re.compile("<tr><td>(\\d+\\.\\d+\\.\\d+\\.\\d+)<SCRIPT type=text/javascript>[^<]+?</SCRIPT></td><td>(.+?)</td><td>")

        proxies = []
        for port in psource_ports:
            page = 0
            hasNext = True
            while hasNext:
                page += 1
                purl = psource_template % (port, page)
                hasNext = self.__loadProxyFromURL(proxies, purl, p_proxy)
        # load from 2 place
        #        for url in proxy_urls:
        #            self.__loadProxyFromURL2(url, p_proxy2)

        return proxies

    def load_proxyServer(self):
        proxies = []
        url = "http://www.proxynova.com/get_proxies.php?proxy_type=2&btn_submit=Download+all+Proxies"
        self.__loadFromProxyServer(proxies, url)
        return proxies


    def __loadFromProxyServer(self, proxies, url):
        print "load proxies from %s " % url
        source = self.html_getter.getHtmlRetry(url, 3)
        source = unicode(source, "UTF-8").encode("UTF-8")
        print source        
        results = source.split("\n")[2:-2]
        count = 0
        if results is not None:
            for x in results:
                result = x.split(":")
                print "hi " + x
                ip = result[0]
                port = result[1]
                print "length:%s ip:%s  port:%s " % (len(result), ip, port)        
                model = ProxyModel(ip, port, "proxyServer")
                proxies.append(model)
                count += 1
        print "---proxyLoader---:load proxy from proxyServer get %s " % count
        
    def __loadProxyFromURL(self, proxies, url, pattern):
        '''Put model into ProxyModel, return has_next_page.'''

        p_nextpage = re.compile("<a href=[^>]*>下一页</a>")  # copy

        print "---proxyloader---:load proxy from %s" % url
        source = self.html_getter.getHtmlRetry(url, 3)
        source = unicode(source, "gbk").encode("UTF-8")
        foundNextPage = p_nextpage.search(source)

        results = pattern.findall(source)
        count = 0
        if results is not None:
            for result in results:
                ip = result[0]
                port = result[1]

                model = ProxyModel(ip, port, result[2].strip().lower())
                model.location = result[3]
                model.validate_date = result[4]
                proxies.append(model)
                count += 1
        print "---proxyloader---:load proxy from %s (get %s)" % (url, count)
        return foundNextPage


    def saveToFile(self, file_abspath, proxies):
        '''Save list of ProxyModel in a file.'''
        if os.path.exists(file_abspath):
            os.remove(file_abspath)
            print "$proxy/> remove %s." % file_abspath

        # write to file
        f = file(file_abspath, "w")
        for proxyModel in proxies:
            f.write(proxyModel.to_line())
            f.write("\n")
        f.close()
        print "$proxy/> write proxies to %s." % f.name

def test_load_proxycn():
    proxyRes = ProxyResource()
    results = proxyRes.load_proxycn()
    for model in results:
        print model
    proxyRes.saveToFile('/tmp/proxies.text', results);

def test_load_5uproxy_net():
    proxyRes = ProxyResource()
    results = proxyRes.load_proxycn()
    for model in results:
        print model
    proxyRes.saveToFile('/tmp/proxies.text', results);

######################################
# Model
######################################
class ProxyModel:
    def __init__(self, ip, port, type):
        self.ip = ip
        self.port = port
        self.type = type
        self.location = None
        self.validate_date = None

        '''
        这个值的作用：PriorityQueue的值。调整策略：
        值为0-100，默认值为50. 当第一次访问不通, 加30分钟不能访问的时间。错误计数＋1
        '''
        self.value = 50                # PriorityQueue Sort Value.
        self.invalid_time = None    # Wait time, don't use this proxy before this time.
        self.cnt_failed = 0
        self.cnt_success = 0
        self.cnt_banned = 0

    def take_a_rest(self, seconds=0, minutes=0):
        self.invalid_time = datetime.datetime.now() + datetime.timedelta(seconds=seconds, minutes=minutes)
        #print "%s - %s = %s" % (datetime.now(), self.invalid_time, datetime.now() > self.invalid_time)

    def isInRest(self):
        if self.invalid_time is None: return False
        if datetime.datetime.now() < self.invalid_time:
            return True
        return False

    def __str__(self):
        return "proxy(%s>%s:%s)" % (self.type, self.ip, self.port)

    def __cmp__(self, other):
        if not isinstance(other, ProxyModel):
            return (-1)
        return cmp(self.value, other.value)

    def to_line(self):
        return "%s:%s\t%s\t%s\t%s\t%s" % (self.ip, self.port, self.type, self.value, self.location, self.validate_date)


class ProxyKey:
    def __init__(self, ip, value):
        self.ip = ip
        self.value = 50

    def __str__(self):
        return "proxykey(%s, %s)" % (self.ip, self.value)

    def __cmp__(self, other):
        if not isinstance(other, ProxyKey):
            return (-1)
        return cmp(self.value, other.value)



######################################
# Web util
######################################
class WebPageDownloader:
    '''Retrieve html from internet by url (optional via a proxy).'''


    def __init__(self):
        self.default_timeout = 40

    #@return: Source Html of url. 
    def getHtmlRetry(self, url, retry=0):
        if retry <= 0: retry = 20 # default retry 20 times.
        html = None
        source = None
        retry_count = 0
        while retry > 0:
            retry -= 1
            retry_count += 1

            error_msg = None
            try:
                proxy_handler = urllib2.ProxyHandler({})
                opener = urllib2.build_opener(proxy_handler)
                opener.addheaders = REQUEST_HEADER
                html = opener.open(url)
                source = html.read()
            except HTTPError, e:
                error_msg = "Error [%s, %s]" % (e, "")
            except URLError, e:
                error_msg = "Error [%s, %s]" % (e.reason, "")
            except:
                error_msg = "Error [%s, %s]" % (sys.exc_info(), "")

            # on error
            if error_msg is not None:
                print "[X] HtmlGetter err:%s, retry:%s." % (error_msg, retry_count)

            if error_msg is None and self.validate_html(html):
                print "[v] success access webpage."
                return source

        #~ end while

        if retry == 0:
            return None # meet max retry times. also None
        print "should not be here."
        return None

    #
    # Validators
    #
    def validate_html(self, html):
        if html is None : return False
        if html.code in HTTPErrors:
            print "error found: %s: %s " % HTTPErrors[html.code]
            return False
        else:
            return True;




######################################
# Constants
######################################

# HTTP Errors found.
HTTPErrors = {
    #100: ('Continue', 'Request received, please continue'),
    #101: ('Switching Protocols', 'Switching to new protocol; obey Upgrade header'),

    #200: ('OK', 'Request fulfilled, document follows'),
    #201: ('Created', 'Document created, URL follows'),
    #202: ('Accepted', 'Request accepted, processing continues off-line'),
    #203: ('Non-Authoritative Information', 'Request fulfilled from cache'),
    #204: ('No Content', 'Request fulfilled, nothing follows'),
    #205: ('Reset Content', 'Clear input form for further input.'),
    #206: ('Partial Content', 'Partial content follows.'),

    #300: ('Multiple Choices', 'Object has several resources -- see URI list'),
    #301: ('Moved Permanently', 'Object moved permanently -- see URI list'),
    #302: ('Found', 'Object moved temporarily -- see URI list'),
    #303: ('See Other', 'Object moved -- see Method and URL list'),
    #304: ('Not Modified', 'Document has not changed since given time'),
    #305: ('Use Proxy', 'You must use proxy specified in Location to access this resource.'),
    #307: ('Temporary Redirect', 'Object moved temporarily -- see URI list'),

    400: ('Bad Request', 'Bad request syntax or unsupported method'),
    401: ('Unauthorized', 'No permission -- see authorization schemes'),
    402: ('Payment Required', 'No payment -- see charging schemes'),
    403: ('Forbidden', 'Request forbidden -- authorization will not help'),
    404: ('Not Found', 'Nothing matches the given URI'),
    405: ('Method Not Allowed', 'Specified method is invalid for this server.'),
    406: ('Not Acceptable', 'URI not available in preferred format.'),
    407: ('Proxy Authentication Required', 'You must authenticate with this proxy before proceeding.'),
    408: ('Request Timeout', 'Request timed out; try again later.'),
    409: ('Conflict', 'Request conflict.'),
    410: ('Gone', 'URI no longer exists and has been permanently removed.'),
    411: ('Length Required', 'Client must specify Content-Length.'),
    412: ('Precondition Failed', 'Precondition in headers is false.'),
    413: ('Request Entity Too Large', 'Entity is too large.'),
    414: ('Request-URI Too Long', 'URI is too long.'),
    415: ('Unsupported Media Type', 'Entity body in unsupported format.'),
    416: ('Requested Range Not Satisfiable', 'Cannot satisfy request range.'),
    417: ('Expectation Failed', 'Expect condition could not be satisfied.'),

    500: ('Internal Server Error', 'Server got itself in trouble'),
    501: ('Not Implemented', 'Server does not support this operation'),
    502: ('Bad Gateway', 'Invalid responses from another server/proxy.'),
    503: ('Service Unavailable', 'The server cannot process the request due to a high load'),
    504: ('Gateway Timeout', 'The gateway server did not receive a timely response'),
    505: ('HTTP Version Not Supported', 'Cannot fulfill request.'),
}



# download parameters
REQUEST_HEADER = [
    ('User-agent', 'Mozilla/5.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; iCafeMedia; .NET CLR 2.0.50727; CIBA)'),
    ('Accept', '*/*'),
    ('Accept-Charset', 'gzip, deflate'),
    ('Cookie', 'Tango_UserReference=38D8FF1624305B16496E9808; MTCCK=1; _csuid=48feeef505683659; cookmcnt=999; CID=1459382; cookMemberName=YunFan; cookMemberID=61448; savedEmail=liyunfan@genscriptcorp.com; DLDExec=OK; __utma=232384002.1655516880.1231991960.1231994793.1232000250.3; __utmb=232384002; __utmc=232384002; __utmz=232384002.1231991960.1.1.utmccn=(direct)|utmcsr=(direct)|utmcmd=(none)'),
#    ('Cookie', 'PREF=ID=ec3c076862e0b02b:U=cac317b6394968ad:LD=en:NR=10:NW=1:CR=2:TM=1330664473:LM=1335417048:GM=1:S=50GQeoV9xkTgrLrN; SS=DQAAAL0AAABvypgyHPqwSw0-rjn-XTDSRpzskVndpZ-rItaXJ7nFuYurPB1psFe9FyVm68eetmO04GnSt_yZ_bx3OZ_cEUcDpt8By3257clGanp-2YNVSvZHYZ5wyBmlh-Y1l8XWV3rLJaqyoXZ5gCZD_sZvrc6WRbGQedkXnMfKGak6rxPKeHp9E9otyK_d4zdLc-y5w2zf2dEQvOUwwxx-tsEkjs2Kd_I09h4qAUB81hORPnx78vFJZ917KoDAdOSzBc8TGWE; HSID=A0_nqPOdpqC042XTn; APISID=Ff1hrOKL1Z7wYBcf/AosfTiZgxii-N7NFo; GSP=ID=ec3c076862e0b02b:IN=e5ffd187aee42e82+8b9a455bd1c58d67:CF=4:UI=1:S=v2gHmeovcUDrBDUT; NID=60=AqhxHbvNGgXuytsC3ZH-hf5Egwye_6UoWoJRrHBSn0hlmb9Zpj5jc7Rf4i7U7gtdKaEk-G4wf_JpZFp6lPwSIhKHcp-MwPLYT1b5HRhBLUJoanR1paNxec6goOGAwPoMYvykytG22FZ4H7lImLG-V9EKGCE6qG8vTmN0NzCBDmCN4D77_B_6qUOi7QI; GDSESS=ID=74c0ae72a299270f:TM=1338800889:C=c:IP=166.111.134.53-:S=ADSvE-cUtJiPIgpC4XwuimeW8fipwOtgEA; SID=DQAAAC4BAAB31ZEj49yN182_gq2_DX6OqtCe9AGhXaD4FwRWtvNZmxBB-d4zctSWtsK_KNQIvH9vJ26dFG1usmUtt8_a1SOP8qFUCnkPnGuDSl8-jkHjBfEOAEKSQBZSOU3qKOsSB05JVTcGvyL3GYUrozeHpDs8GaAafpJdlxNln85ZGS_WPHgNbvSl5fbisovVV1xNPRhilfxFU5tTluitFWh_0L5dtPgFKmbiV4wKEAV2xTef5VDVAro3JjLgQRVJciNqLFJxvgYCJet6AaxQRKYGl97P_KCb3CRWzLE5c918YBEsgIHyxp-93tZS9xPryjkXSCsG1N95h2DzkaxeQaa13X-hwSohxk2feW8jkAlGLv2IL3J1RNzIg8c0EsMIdUXYE8nMgi-mCr5dJDEZXwWXa3nE'),
    ('Accept-Language', 'en')
]


######################################
# Main
######################################
if __name__ == "__main__":
    proxyRes = ProxyResource()
    results = proxyRes.load_proxycn()
    with open("proxy.py", 'w') as f:
        f.write("PROXIES = [\n")
        for model in results:
            print model
            f.write("\t\t\t{\"ip_port\":\"%s:%s\"},\n" % (model.ip, model.port))
        f.write("]\n")
