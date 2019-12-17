import requests
import threading
from termcolor import cprint

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
        headers = {"User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.75 Safari/537.36"}
        jboss_url = url + '/invoker/JMXInvokerServlet'
        try:
            r = requests.get(url=jboss_url, headers=headers, timeout=10)
            if r.status_code == 200:
                if r.headers['content-type'].count('serialized') or r.headers['Content-Type'].count('serialized'):
                    cprint('[Jboss] {}'.format(url), 'red')
                    self.vul_list.append(['Jboss', url, 'Yes'])
            else:
                pass
        except Exception as e:
            pass
