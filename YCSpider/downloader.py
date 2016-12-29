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

    def working(self, url, meta=None):
        time.sleep(random.randint(0, self.sleep_time))
        code = 1
        content = None
        try:
            content = self.get_html(url, meta)
        except Exception as excep:
            code = -1  # 重试
        return code, content

    def get_html(self, url, meta=None):
        response = requests.get(url, params=None, data=None, headers=None, cookies=None, timeout=(3.05, 10))
        if response.history:
            # 判断是否重定向
            pass
        content = (url, meta, response)
        return content
