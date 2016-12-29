# _*_ coding: utf-8 _*_

import redis


class Saver(object):
    """
    保存数据
    """

    def __init__(self, host='localhost', port=6379, rediskey='YCSpider:item'):
        self.redisclient = redis.Redis(host, port)
        self.rediskey = rediskey
        return

    def working(self, item):
        try:
            result = self.item_save(item)
        except Exception as excep:
            # 重试
            result = False
        return result

    def item_save(self, item=None):
        self.redisclient.rpush(self.rediskey, item)
        return True
