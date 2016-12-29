# -*- encoding: utf-8 -*-

# 1 获取单条URL 加入到 任务列表中

# 2 下载器 downloader 从任务列表中取出一条 需要下载HTML的任务，下载完成后 把信息放到任务列表中

# 3 网页解析器 parser 从任务列表中取出一条 需要解析的任务 解析完成后 把信息放到任务列表中

# 4 数据存储 save 从任务列表中取出结果 存储到指定位置




# ############################################
# spider start
# 初始化10个线程/进程 读取URL队列 加入 任务列表中
# 初始化10个线程/进程 downloader 开始下载URL列表
# 初始化10个线程/进程 parser 开始解析HTML
# 初始化10个线程/进程 save 保存数据
import Queue
import json
import threading
import time
import redis
from .engine import DownloadThread, ParseThread, SaveThread
from . import config_default


class Console(object):
    """
    控制器 启动采集
    """

    def __init__(self, downloader, parser, saver, spider_name='yc_spider', url_filter=None, pool_type="thread"):
        assert pool_type == 'thread', 'ConcurPool: pool_type must be "thread"'
        self.spider_name = spider_name
        self.pool_type = pool_type

        self.downloader = downloader  # 抓取
        self.parser = parser  # 解析
        self.saver = saver  # 保存
        self.url_filter = url_filter
        # 线程队列
        self.downloader_queue = Queue.Queue()
        self.parse_queue = Queue.Queue()
        self.save_queue = Queue.Queue()
        self.lock = threading.Lock()
        # 配置
        self.configs = config_default.configs
        try:
            from . import config_override
            self.configs = self.merge(self.configs, config_override.configs)
        except:
            pass
        self.load_config()

        return

    def load_config(self):
        self.redishost = self.configs.get('redis').get('host', '127.0.0.1')
        self.port = self.configs.get('redis').get('port', 6379)
        self.urls_key = self.configs.get('redis').get('urls_key', '%s:start_url') % self.spider_name
        self.item_key = self.configs.get('redis').get('item_key', '%s:item') % self.spider_name
        self.redisclient = redis.Redis(self.redishost, self.port)

        self.download_num = self.configs.get('crawl').get('download_num', 10)
        self.parser_num = self.configs.get('crawl').get('parser_num', 2)
        self.saver_num = self.configs.get('crawl').get('saver_num', 1)

    def merge(self, defaults, override):
        r = {}
        for k, v in defaults.items():
            if k in override:
                if isinstance(v, dict):
                    r[k] = self.merge(v, override[k])
                else:
                    r[k] = override[k]
            else:
                r[k] = v
        return r

    def set_start_url(self, taskinfo):
        self.add_a_task("downloader", taskinfo)
        return

    def add_crawl_urls(self, task_list=[]):
        for task in task_list:
            taskinfo = json.loads(task)
            self.add_a_task("downloader", taskinfo)
        while True:
            task = self.redisclient.rpop(self.urls_key)
            if task:
                taskinfo = json.loads(task)
                self.set_start_url(taskinfo)
            else:
                time.sleep(5)
            time.sleep(0.1)

    def start_work_and_wait_done(self, download_num=None):
        if not download_num:
            self.download_num = download_num
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
        if task_name == "downloader":
            self.downloader_queue.put(task_content, block=True)
        elif task_name == "parser":
            self.parse_queue.put(task_content, block=True)
        elif task_name == "saver":
            self.save_queue.put(task_content, block=True)
        else:
            print "错误的task类型"
        return

    def get_a_task(self, task_name):
        task_content = None
        while True:
            try:
                if task_name == "downloader":
                    task_content = self.downloader_queue.get(block=True, timeout=5)  # (url,meta=None)
                elif task_name == "parser":
                    # print 'parser 队列长度：', self.parse_queue.qsize()
                    task_content = self.parse_queue.get(block=True, timeout=5)  # (url, meta, response)
                elif task_name == "saver":
                    task_content = self.save_queue.get(block=True, timeout=5)
                break
            except:
                time.sleep(5)
        return task_content

    def finish_a_task(self, task_name):
        if task_name == "downloader":
            self.downloader_queue.task_done()
        elif task_name == "parser":
            self.parse_queue.task_done()
        elif task_name == "saver":
            self.save_queue.task_done()
        else:
            pass
        return
