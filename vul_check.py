import sys
import threading

from plugins import *
from termcolor import cprint
from queue import Queue

vul_list = []
web_queue = []


with open(sys.argv[1], "r") as f:
    for i in f.readlines():
        web_queue.append(i.strip())
    f.close()

for vulClass in [shiro,weblogic,struts2]:
    detect = vulClass.Detect
    cprint('-' * 50 + 'detect ' + detect.name + '-' * 50, 'green')  # 探测各种漏洞
    try:
        alive_Web_queue = Queue(-1)  # 将存活的web存入队列里
        for _ in web_queue:
            alive_Web_queue.put(_)

        threads = []
        thread_num = 50  # 漏洞检测的线程数目
        for num in range(1, thread_num + 1):
            t = detect(alive_Web_queue, vul_list)  # 实例化漏洞类，传递参数：存活web的队列，  存储漏洞的列表
            threads.append(t)
            t.start()
        for t in threads:
            t.join()
    except Exception as e:
        print(r'[-] Load Vul [{}] Error: {}'.format(detect.name, e.args))
        continue
