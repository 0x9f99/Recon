import requests
import threading
from termcolor import cprint
from urllib.parse import urlparse

class Detect(threading.Thread):
    def __init__(self, alive_Web_queue, vul_list):
        threading.Thread.__init__(self)
        self.alive_Web_queue = alive_Web_queue      # 存活web的队列
        self.vul_list = vul_list                    # 存储漏洞的名字和url


    def run(self):
        while not self.alive_Web_queue.empty():
            alive_web = self.alive_Web_queue.get()
            self.run_detect(alive_web)

    # 只需要修改下面的代码就行
    def run_detect(self, url):
        if not urlparse(url).scheme:
            url = 'https://' + url
        else:
            url = url
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:46.0) Gecko/20100101 Firefox/46.0'}
        weblogic_url = url + '/_async/AsyncResponseService'
        try:
            res = requests.get(url=weblogic_url, headers=headers, allow_redirects=False, timeout=10)
            if 'AsyncResponseService home page' in res.text:
                cprint('[weblogic] {}'.format(url), 'red')
                self.vul_list.append(['weblogic', url])
            else:
                print('[-] {}'.format(url))
        except Exception as e:
            pass
            #print('[error] {}: {}'.format(url, e.args))