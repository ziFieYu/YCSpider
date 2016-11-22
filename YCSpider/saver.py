# _*_ coding: utf-8 _*_
import sys


class Saver(object):
    """
    保存数据
    """

    def __init__(self, file_name=None):
        self.file_name = file_name  # default: None, output file or sys.stdout(if file_name is None)
        self.save_pipe = open(file_name, "w", encoding="utf-8") if file_name else sys.stdout
        return

    def working(self, url, keys, item):
        try:
            result = self.item_save(url, keys, item)
        except Exception as excep:
            # 重试
            result = False
        return result

    def item_save(self, url, keys, item):
        self.save_pipe.write("\t".join([url, str(keys), "\t".join([str(i) for i in item])]) + "\n")
        self.save_pipe.flush()
        return True
