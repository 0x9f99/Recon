import requests
import threading
import re
from termcolor import cprint
from urllib.parse import urlparse

class Detect(threading.Thread):
    def __init__(self, alive_Web_queue, vul_list):
        threading.Thread.__init__(self)
        self.alive_Web_queue = alive_Web_queue    # 存活web的队列
        self.vul_list = vul_list    # 存储漏洞的名字和url
        self.struts2_patten = re.compile(r'''["']([\S]+?\.(action|do))''', re.IGNORECASE)
        
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

        struts2_url = ''
        try:
            res = requests.get(url=url, headers=headers, timeout=10)
            redirect_url = res.url
            # print('[redirect to] {}'.format(redirect_url))
            html_doc = res.text
            if '.action' in urlparse(redirect_url).path or '.do' in urlparse(redirect_url).path:
                struts2_url = redirect_url
                cprint('[struts2] {}'.format(struts2_url),'red')
                self.vul_list.append(['struts2', struts2_url])
            elif '.action' in html_doc or '.do' in html_doc:
                try:
                    action_do_link = re.search(self.struts2_patten, html_doc).group(1)
                    struts2_url = redirect_url + '/' + action_do_link
                    cprint('[struts2 in html] {}'.format(struts2_url),'red')
                    self.vul_list.append(['struts2', struts2_url])
                except Exception as e:
                    pass
        except Exception as e:
            pass
