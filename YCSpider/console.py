# -*- encoding: utf-8 -*-
import Queue
import json
import threading
import time
import redis
from .engine import DownloadThread, ParseThread, SaveThread
from . import downloader, config_default


class Console(object):
    """
    控制器 启动采集
    """

    def __init__(self, parser, saver, spider_name):
        '''
        构造函数

        :param parser:解析数据的方法对象
        :param saver:存储数据的方法对象
        :param spider_name:爬虫名称
        '''
        self.spider_name = spider_name
        self.downloader = downloader.Downloader()
        self.parser = parser
        self.saver = saver
        # 线程队列
        self.downloader_queue = Queue.Queue()
        self.parse_queue = Queue.Queue()
        self.save_queue = Queue.Queue()
        # self.lock = threading.Lock()
        # 加载配置信息
        self.load_config()
        return

    def load_config(self):
        '''
        加载配置信息
        :return:
        '''
        self.configs = config_default.configs
        try:
            from . import config_override
            self.configs = self.merge(self.configs, config_override.configs)
        except:
            pass
        self.redishost = self.configs.get('redis').get('host', '127.0.0.1')
        self.port = self.configs.get('redis').get('port', 6379)
        self.urls_key = self.configs.get('redis').get('urls_key', '%s:start_url') % self.spider_name
        self.item_key = self.configs.get('redis').get('item_key', '%s:item') % self.spider_name
        self.redisclient = redis.Redis(self.redishost, self.port)
        self.download_num = self.configs.get('crawl').get('download_num', 10)
        self.parser_num = self.configs.get('crawl').get('parser_num', 2)
        self.saver_num = self.configs.get('crawl').get('saver_num', 1)

    def merge(self, defaults, user_conf):
        '''
        使用用户配置覆盖默认配置
        :param defaults:默认配置
        :param override:用户配置
        :return:
        '''
        r = {}
        for k, v in defaults.items():
            if k in user_conf:
                if isinstance(v, dict):
                    r[k] = self.merge(v, user_conf[k])
                else:
                    r[k] = user_conf[k]
            else:
                r[k] = v
        return r

    def add_crawl_urls(self, task_list=[], headers=None):
        '''
        添加task到采集队列中
        :param task_list:默认task列表
        :param headers:请求头
        :return:
        '''

        for task in task_list:
            taskinfo = json.loads(task)
            self.add_a_task("downloader", (taskinfo, headers, self.parser))
        while True:
            task = self.redisclient.rpop(self.urls_key)
            if task:
                taskinfo = json.loads(task)
                self.add_a_task("downloader", (taskinfo, headers, self.parser))
            else:
                time.sleep(5)
            time.sleep(1)

    def start_work_and_wait_done(self):
        '''
        开始启动爬虫
        :return:
        '''
        threads_list = [DownloadThread("downloader-%d" % i, self.downloader, self) for i in range(self.download_num)] + \
                       [ParseThread("parser-%d" % i, self.parser, self) for i in range(self.parser_num)] + \
                       [SaveThread("saver-%d" % i, self.saver, self) for i in range(self.saver_num)]

        for thread in threads_list:
            thread.setDaemon(True)
            thread.start()

        for thread in threads_list:
            if thread.is_alive():
                thread.join()

        return

    ########################################################################################################

    def add_a_task(self, task_name, task_content):
        '''
        基本功能 - 添加一个任务到指定队列中
        :param task_name: 任务名称
        :param task_content: 任务类型
        :return:
        '''
        assert task_name, 'add_a_task: task_name not empty'
        if task_name == "downloader":
            self.downloader_queue.put(task_content, block=True)
        elif task_name == "parser":
            self.parse_queue.put(task_content, block=True)
        elif task_name == "saver":
            self.save_queue.put(task_content, block=True)
        return

    def get_a_task(self, task_name):
        '''
        根据task_name 从指定队列中取一个一条任务 并返回
        :param task_name:任务名称
        :return:返回任务信息
        '''

        assert task_name, 'get_a_task: task_name not empty'
        if task_name == "downloader":
            task_content = self.downloader_queue.get(block=True, timeout=5)  # (url,meta=None)
        elif task_name == "parser":
            task_content = self.parse_queue.get(block=True, timeout=5)  # (url, meta, response)
        elif task_name == "saver":
            task_content = self.save_queue.get(block=True, timeout=5)
        return task_content

    def finish_a_task(self, task_name):
        '''
        完成一条任务
        :param task_name: 任务名称
        :return:
        '''
        assert task_name, 'finish_a_task: task_name not empty'
        if task_name == "downloader":
            self.downloader_queue.task_done()
        elif task_name == "parser":
            self.parse_queue.task_done()
        elif task_name == "saver":
            self.save_queue.task_done()
        else:
            pass
        return
