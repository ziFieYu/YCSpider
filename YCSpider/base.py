# -*- encoding: utf-8 -*-
import multiprocessing
import threading
import Queue


class BaseConcur(object):
    """
    class of BaseConcur, as base class of BaseThread and BaseProcess
    """

    def __init__(self, name, worker, pool):
        """
        constructor
        """
        self.name = name        # the name of each thread or process
        self.worker = worker    # the worker of each thread or process
        self.pool = pool        # thread_pool or process_pool
        return

    def run(self):
        """
        rewrite run function of Thread or Process, auto running, and must call self.work()
        """

        while True:
            try:
                if not self.work():
                    break
            except Queue.Empty:
                if self.pool.is_all_tasks_done():
                    break
        return

    def work(self):
        """
        procedure of each thread or process, return True to continue, False to stop
        """
        assert False, "you must rewrite work function in subclass of %s" % self.__class__.__name__


class BaseThread(BaseConcur, threading.Thread):
    """
    class of BaseThread, as base class of each thread
    """

    def __init__(self, name, worker, pool):
        """
        constructor
        """
        threading.Thread.__init__(self, name=name)
        BaseConcur.__init__(self, name, worker, pool)
        return


class BaseProcess(BaseConcur, multiprocessing.Process):
    """
    class of BaseProcess, as base class of each process
    """

    def __init__(self, name, worker, pool):
        """
        constructor
        """
        multiprocessing.Process.__init__(self, name=name)
        BaseConcur.__init__(self, name, worker, pool)
        return
