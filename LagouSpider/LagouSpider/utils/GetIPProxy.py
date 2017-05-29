# -*- coding: utf-8 -*-

import requests
import json

if __name__ == "__main__":
    r = requests.get('http://127.0.0.1:8000/?types=0&protocol=0&count=600&country=国内')
    ip_ports = json.loads(r.text)

    print(ip_ports)
    ip = ip_ports[0][0]
    port = ip_ports[0][1]
    # proxies={
    #     'http':'http://%s:%s'%(ip,port),
    #     'https':'http://%s:%s'%(ip,port)
    # }
    proxies = {'http':'http://%s:%s'%(ip, port)}

    r = requests.get('http://icanhazip.com/',proxies=proxies)
    r.encoding='utf-8'
    print(r.text)

    # r = requests.get('http://127.0.0.1:8000/delete?count=100')
    # print(r.text)
