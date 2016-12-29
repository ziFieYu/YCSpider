# -*- encoding: utf-8 -*-

import YCSpider


class crawl():
    def __init__(self):
        self.downloader = YCSpider.Downloader()
        self.url = ''
        self.meta = {}


    def start(self):
        self.downloader.working(self.url, self.meta)
