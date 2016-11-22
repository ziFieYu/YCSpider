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
import multiprocessing
import threading

from .engine import DownloadThread, ParseThread, SaveThread, DownloadProcess, ParseProcess, SaveProcess


class Console(object):
    """
    控制器 启动采集
    """

    def __init__(self, downloader, parser, saver, url_filter=None, monitor_sleep_time=5, pool_type="thread"):
        assert pool_type in ("thread", "process"), "ConcurPool: pool_type must be 'thread' or 'process'"
        self.pool_name = "ThreadPool" if pool_type == "thread" else "ProcessPool"
        self.pool_type = pool_type  # default: "thread", must be "thread" or "process", to identify pool type

        self.downloader = downloader  # 抓取
        self.parser = parser  # 解析
        self.saver = saver  # 保存
        self.url_filter = url_filter  # default: None, also can be UrlFilter()

        # define different variables based on self.pool_type
        if self.pool_type == "thread":
            self.downloader_queue = Queue.PriorityQueue()
            self.parse_queue = Queue.PriorityQueue()
            self.save_queue = Queue.Queue()
            self.lock = threading.Lock()
        else:
            self.downloader_queue = multiprocessing.JoinableQueue()
            self.parse_queue = multiprocessing.JoinableQueue()
            self.save_queue = multiprocessing.JoinableQueue()

            self.manager = multiprocessing.Manager()  # use multiprocessing.Manager to share memory
            self.number_dict = self.manager.dict(self.number_dict)  # change self.number_dict based on self.manager
            self.lock = multiprocessing.Lock()  # the lock which self.number_dict needs

        # 线程or进程 监控
        # self.monitor_stop = False
        # self.monitor = MonitorThread("monitor", self, sleep_time=monitor_sleep_time)
        # self.monitor.setDaemon(True)
        # self.monitor.start()
        return

    def set_start_url(self, url):
        self.add_a_task("downloader", url)
        return

    def start_work_and_wait_done(self, download_num=10, parser_num=1):

        if self.pool_type == "thread":
            threads_list = [DownloadThread("downloader-%d" % i, self.downloader, self) for i in range(download_num)] + \
                           [ParseThread("parser", self.parser, self)] + \
                           [SaveThread("saver", self.saver, self)]
            process_list = []
        else:
            threads_list = [DownloadProcess("downloader-%d" % i, self.downloader, self) for i in range(download_num)]
            process_list = [ParseProcess("parser-%d" % i, self.parser, self) for i in range(parser_num)] + \
                           [SaveProcess("saver", self.saver, self)]

        for thread in threads_list:
            thread.setDaemon(True)
            thread.start()

        for process in process_list:
            process.daemon = True
            process.start()

        for thread in threads_list:
            if thread.is_alive():
                thread.join()

        for process in process_list:
            if process.is_alive():
                process.join()

        # 监控
        # if is_over and self.monitor.is_alive():
        #     self.monitor_stop = True
        #     self.monitor.join()
        return

    ########################################################################################################

    def add_a_task(self, task_name, task_content):
        """
        add a task based on task_name, if queue is full, blocking the queue
        """
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
        """
        get a task based on task_name, if queue is empty, raise queue.Empty
        """
        task_content = None
        if task_name == "downloader":
            task_content = self.downloader_queue.get(block=True, timeout=5)
        elif task_name == "parser":
            task_content = self.parse_queue.get(block=True, timeout=5)
        elif task_name == "saver":
            task_content = self.save_queue.get(block=True, timeout=5)
        else:
            pass
            # logging.error("%s get_a_task error: parameter[%s] is invalid", self.pool_name, task_name)
        return task_content

    def finish_a_task(self, task_name):
        """
        finish a task based on task_name, call queue.task_done()
        """
        if task_name == "downloader":
            self.fetch_queue.task_done()
        elif task_name == "parser":
            self.parse_queue.task_done()
        elif task_name == "saver":
            self.save_queue.task_done()
        else:
            pass
        return
        ########################################################################################################
