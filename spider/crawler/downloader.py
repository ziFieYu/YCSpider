# _*_ coding: utf-8 _*_
import random
import time

import requests


class Downloader(object):
    """
    Downloader,to download html
    """

    def __init__(self, max_repeat=3, sleep_time=1):
        self.max_repeat = max_repeat
        self.sleep_time = sleep_time

    def working(self, url, repeat):
        time.sleep(random.randint(0, self.sleep_time))
        try:
            content = self.get_html(url)
        except Exception as excep:
            print excep
            if (repeat > self.max_repeat):
                content = None
                # break repeat
            else:
                content = None
                # add to queue for continue repeat

        # logging.debug("Fetcher end: code=%s, url=%s", code, url)
        return content

    def get_html(self, url):
        headers = {
            # "User-Agent": make_random_useragent(), # 随机请求头
            "Accept-Encoding": "gzip",
        }
        response = requests.get(url, params=None, data=None, headers=headers, cookies=None, timeout=(3.05, 10))
        if response.history:
            # logging.debug("Fetcher redirect: keys=%s, critical=%s, fetch_repeat=%s, url=%s", keys, critical, fetch_repeat, url)
            pass
        content = (response.status_code, response.url, response.text)
        return content
