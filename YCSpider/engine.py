# -*- encoding: utf-8 -*-

from .base import BaseThread


# =========================  下载器  =========================
def work_download(self):
    # ----1 获取要下载的task
    meta = self.pool.get_a_task("downloader")
    url = meta.get('url', '')

    # ----2 发送request请求 得到response
    code, response = self.worker.working(url, meta)
    meta = response[1]
    response = response[2]

    # ----3 判断response状态码 选择后续动作
    if code == 1:
        self.pool.add_a_task("parser", (url, meta, response))
    elif code == -1:
        # 获取网页源代码失败 重试
        self.pool.add_a_task("downloader", (url, meta))

    # ----4
    self.pool.finish_a_task("downloader")
    return True


DownloadThread = type("DownloadThread", (BaseThread,), dict(work=work_download))


# =========================  解析器  =========================
def work_parse(self):
    # ----1 获取要解析的task (url, meta, response)
    url, meta, response = self.pool.get_a_task("parser")
    # ----2 开始解析
    code, url_list, save_list = self.worker.working(url, meta, response)

    # ----3 判断解析状态 选择后续操作
    if code == 1:
        for _url, _meta in url_list:
            self.pool.add_a_task("downloader", (_url, _meta))
        for item in save_list:
            # print item
            self.pool.add_a_task("saver", item)
    elif code == -1:
        self.pool.add_a_task("downloader", (url, meta))
    else:
        pass

    # ----4
    self.pool.finish_a_task("parser")
    return True


ParseThread = type("ParseThread", (BaseThread,), dict(work=work_parse))


# =========================  存储器  =========================
def work_save(self):
    # ----1 获取要存储的task
    item = self.pool.get_a_task("saver")

    # ----2 存储
    result = self.worker.working(item)

    # ----3 判断存储结果 选择后续操作
    if result:
        pass
    # ----4
    self.pool.finish_a_task("saver")
    return True


SaveThread = type("SaveThread", (BaseThread,), dict(work=work_save))
