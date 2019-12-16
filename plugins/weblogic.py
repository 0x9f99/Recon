import requests
import threading
from termcolor import cprint
from urllib.parse import urlparse

class Detect(threading.Thread):
    def __init__(self, alive_Web_queue, vul_list):
        threading.Thread.__init__(self)
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:46.0) Gecko/20100101 Firefox/46.0'}
        self.alive_Web_queue = alive_Web_queue
        self.vul_list = vul_list


    def run(self):
        while not self.alive_Web_queue.empty():
            alive_web = self.alive_Web_queue.get()
            self.run_detect(alive_web)

    def CVE_2017_10271(self,url):
        weblogic_url = url + '/wls-wsat/CoordinatorPortType'
        try:
            res = requests.get(url=weblogic_url, headers=self.headers, allow_redirects=False, timeout=10)
            if 'CoordinatorPortType?wsdl' in res.text:
                cprint('[CVE_2017_10271] {}'.format(url), 'red')
                self.vul_list.append(['weblogic', url])
            else:
                print('[-] {}'.format(url))
        except Exception as e:
            pass
    
    def CVE_2019_2725(self,url):
        weblogic_url = url + '/_async/AsyncResponseService'
        try:
            res = requests.get(url=weblogic_url, headers=self.headers, allow_redirects=False, timeout=10)
            if 'AsyncResponseService home page' in res.text:
                cprint('[CVE-2019-2725] {}'.format(url), 'red')
                self.vul_list.append(['weblogic', url])
            else:
                print('[-] {}'.format(url))
        except Exception as e:
            pass
     
    def CVE_2019_2729(self,url):
        weblogic_url = url + '/wls-wsat/CoordinatorPortType11'
        try:
            res = requests.get(url=weblogic_url, headers=self.headers, allow_redirects=False, timeout=10)
            if 'CoordinatorPortType11?wsdl' in res.text:
                cprint('[CVE-2019-2729] {}'.format(url), 'red')
                self.vul_list.append(['weblogic', url])
            else:
                print('[-] {}'.format(url))
        except Exception as e:
            pass

    def run_detect(self, url):
        if not urlparse(url).scheme:
            url = 'https://' + url
        else:
            url = url
            
        self.CVE_2017_10271(url)
        self.CVE_2019_2725(url)
        self.CVE_2019_2729(url)
