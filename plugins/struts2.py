import requests
import threading
from termcolor import cprint
import re
from urllib.parse import urlparse

class Detect(threading.Thread):
    def __init__(self, alive_Web_queue, vul_list):
        threading.Thread.__init__(self)
        self.alive_Web_queue = alive_Web_queue      # 存活web的队列
        self.vul_list = vul_list                    # 存储漏洞的名字和url
        self.struts2_patten = re.compile(r'''["']([\S]+?\.(action|do))''', re.IGNORECASE)

    def run(self):
        while not self.alive_Web_queue.empty():
            alive_web = self.alive_Web_queue.get()
            self.run_detect(alive_web)

    # 只需要修改下面的代码就行
    def run_detect(self, url):
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:46.0) Gecko/20100101 Firefox/46.0'}

        struts2_url = ''

        try:
            res = requests.get(url=url, headers=headers, timeout=10)
            redirect_url = res.url                  # 跳转后的url
            # print('[redirect to] {}'.format(redirect_url))
            html_doc = res.text
            if '.action' in urlparse(redirect_url).path:            # 跳转后的url带有action或者do
                struts2_url = redirect_url
                print('[+1] {}'.format(struts2_url))
            elif '.action' in html_doc:                # 网页源码里有action或者do，并正则匹配出链接
                try:
                    action_do_link = re.search(self.struts2_patten, html_doc).group(1)
                    struts2_url = redirect_url + '/' + action_do_link
                    print('[+2] {}'.format(struts2_url))
                except Exception as e:
                    pass

