from plugins import *
import sys
import threading

from queue import Queue

alive_Web_queue = Queue(-1)
vul_list = []
web_queue = []


with open(sys.argv[1], "r") as f:
    for i in f.readlines():
        web_queue.append(i.strip())
    f.close()

for q in web_queue:
    alive_Web_queue.put(q)


shiro_check = shiro.Detect(alive_Web_queue,vul_list)
weblogic_check = weblogic.Detect(alive_Web_queue,vul_list)
shiro=threading.Thread(target=weblogic_check.run)
weblogic=threading.Thread(target=weblogic_check.run)

shiro.start()
weblogic.start()
#shiro_check.run()
#weblogic_check.run()
