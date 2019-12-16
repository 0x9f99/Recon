import requests
import threading
from termcolor import cprint
from urllib.parse import urlparse


class Detect(threading.Thread):
    def __init__(self, alive_Web_queue, vul_list):
        threading.Thread.__init__(self)
        self.alive_Web_queue = alive_Web_queue
        self.vul_list = vul_list

    def run(self):
        while not self.alive_Web_queue.empty():
            alive_web = self.alive_Web_queue.get()
            self.run_detect(alive_web)

    def run_detect(self, url):
        if not urlparse(url).scheme:
            url = 'https://' + url
        else:
            url = url
        
        shiro_headers = {'Cookie': 'rememberMe=1','User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:46.0) Gecko/20100101 Firefox/46.0'}
        
        try:
            res = requests.get(url=url, headers=shiro_headers, allow_redirects=False, timeout=10)
            res_setcookies = res.headers['Set-Cookie']
            if 'rememberMe=deleteMe' in res_setcookies:
                cprint('[shiro] {}'.format(url), 'blue')
                self.vul_list.append(['shiro', url])
                #isShiroList.append(url)
            else:
                print('[-] {}'.format(url))
        except Exception as e:
            pass
            #print('[-] {}'.format(url))
