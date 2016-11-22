# -*- encoding: utf-8 -*-

from .base import BaseThread, BaseProcess


# ===============================================================================================================================
def work_download(self):
    # ----1
    priority, url, keys, deep, critical, fetch_repeat, parse_repeat = self.pool.get_a_task("downloader")

    # ----2
    code, content = self.worker.working(url, keys, critical, fetch_repeat)

    # ----3
    if code > 0:
        self.pool.add_a_task("parser", (priority, url, keys, deep, critical, fetch_repeat, parse_repeat, content))
    elif code == 0:
        priority += (1 if critical else 0)
        self.pool.add_a_task("downloader", (priority, url, keys, deep, critical, fetch_repeat + 1, parse_repeat))
    else:
        pass

    # ----4
    self.pool.finish_a_task("downloader")
    return True


DownloadThread = type("FetchThread", (BaseThread,), dict(work=work_download))
DownloadProcess = type("FetchProcess", (BaseProcess,), dict(work=work_download))


# ===============================================================================================================================
def work_parse(self):
    # ----1
    priority, url, keys, deep, critical, fetch_repeat, parse_repeat, content = self.pool.get_a_task("parser")

    # ----2
    code, url_list, save_list = self.worker.working(priority, url, keys, deep, critical, parse_repeat, content)

    # ----3
    if code > 0:
        for _url, _keys, _critical, _priority in url_list:
            self.pool.add_a_task("downloader", (_priority, _url, _keys, deep + 1, _critical, 0, 0))
        for item in save_list:
            self.pool.add_a_task("saver", (url, keys, item))
    elif code == 0:
        priority += (1 if critical else 0)
        self.pool.add_a_task("downloader", (priority, url, keys, deep, critical, fetch_repeat, parse_repeat + 1))
    else:
        pass

    # ----4
    self.pool.finish_a_task("parser")
    return True


ParseThread = type("ParseThread", (BaseThread,), dict(work=work_parse))
ParseProcess = type("ParseProcess", (BaseProcess,), dict(work=work_parse))


# ===============================================================================================================================
def work_save(self):
    # ----1
    url, keys, item = self.pool.get_a_task("saver")

    # ----2
    result = self.worker.working(url, keys, item)

    # ----3
    if result:
        pass
    # ----4
    self.pool.finish_a_task("saver")
    return True


SaveThread = type("SaveThread", (BaseThread,), dict(work=work_save))
SaveProcess = type("SaveProcess", (BaseProcess,), dict(work=work_save))
