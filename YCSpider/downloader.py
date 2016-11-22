# _*_ coding: utf-8 _*_
import random
import time

import requests


class Downloader(object):
    """
    下载器
    """

    def __init__(self, sleep_time=1):
        self.sleep_time = sleep_time

    def working(self, url):
        time.sleep(random.randint(0, self.sleep_time))
        try:
            content = self.get_html(url)
        except Exception as excep:
            print excep
            # 重试
        return content

    def get_html(self, url):
        headers = {
            "Accept-Encoding": "gzip",
        }
        response = requests.get(url, params=None, data=None, headers=headers, cookies=None, timeout=(3.05, 10))
        if response.history:
            # 判断是否重定向
            pass
        content = (response.status_code, response.url, response.text)
        return content
