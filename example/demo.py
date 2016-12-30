# -*- encoding: utf-8 -*-
import re
import sys
import threading
import redis
import requests
import YCSpider
from YCSpider import config_default

reload(sys)
sys.setdefaultencoding('utf-8')


# 定义解析过程
class TMParser(YCSpider.Parser):
    def htm_parse(self, url, meta, response):
        url_list, saver_list = [], []
        item = {}
        cur_html = str(response.text)
        pattern = 'keywords" content="(?P<title>.*?)"'
        title = re.search(pattern, cur_html).group('title')
        item['url'] = meta.get('url', '')
        item['category1'] = meta.get('category1', '')
        item['brand'] = meta.get('brand', '')
        item['title'] = title
        saver_list.append(item)
        return url_list, saver_list



# 定义保存过程
class TMSaver(YCSpider.Saver):
    def __init__(self, host='localhost', port=6379, rediskey=''):
        self.redisclient = redis.Redis(host, port)
        self.rediskey = rediskey

    def item_save(self, item):
        try:
            self.redisclient.lpush(self.rediskey, item)
        except Exception as e:
            return False
        return True


if __name__ == "__main__":
    spider_name = 'yc_spider'

    configs = config_default.configs
    redishost = configs.get('redis').get('host', '127.0.0.1')
    port = configs.get('redis').get('port', 6379)
    rediskey = configs.get('redis').get('item_key', '%s:item') % spider_name

    # 初始化parser和saver
    parser = TMParser()
    saver = TMSaver(host=redishost, port=port, rediskey=rediskey)

    # 初始化爬虫, 并传入初始Url
    nba_spider = YCSpider.WebSpider(parser, saver, spider_name='yc_spider')

    t1 = threading.Thread(target=nba_spider.add_crawl_urls)
    t1.setDaemon(True)
    t1.start()

    # 开启10个线程抓取数据
    nba_spider.start_work_and_wait_done()

    t1.join()

    # exit()
