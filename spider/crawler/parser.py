# _*_ coding: utf-8 _*_

import re
import random
import logging
import datetime


class Parser(object):
    """
    Parser,to parse html
    """

    def __init__(self, max_deep=0, max_repeat=3):
        self.max_deep = max_deep  # default: 0, if -1, spider will not stop until all urls are fetched
        self.max_repeat = max_repeat  # default: 3, maximum repeat time for parsing content
        self.log_str_format = "priority=%s, keys=%s, deep=%s, critical=%s, parse_repeat=%s, url=%s"
        return

    def working(self, priority, url, keys, deep, parse_repeat, content):
        """
        working function, must "try, except" and call self.htm_parse(), don't change parameters and return
        :param priority: the priority of this url, which can be used in this function
        :param keys: some information of this url, which can be used in this function
        :param deep: the deep of this url, which can be used in this function
        :param parse_repeat: the parse repeat time of this url, if parse_repeat >= self.max_repeat, return code = -1
        :param content: the content of this url, which needs to be parsed, content is a tuple or list
        :return (code, url_list, save_list): url_list is [(url, keys, critical, priority), ...], save_list is [item, ...]
        """
        # logging.debug("Parser start: %s", self.log_str_format % (priority, keys, deep, parse_repeat, url))

        try:
            url_list, save_list = self.htm_parse(priority, url, keys, deep, parse_repeat, content)
        except Exception as excep:
            if parse_repeat >= self.max_repeat:
                url_list, save_list = [], []
                # logging.error("Parser error: %s, %s", excep, self.log_str_format % (priority, keys, deep, parse_repeat, url))
            else:
                url_list, save_list = [], []
                # logging.debug("Parser repeat: %s, %s", excep, self.log_str_format % (priority, keys, deep, parse_repeat, url))

        # logging.debug("Parser end: code=%s, len(url_list)=%s, len(save_list)=%s, url=%s", code, len(url_list), len(save_list), url)
        return url_list, save_list

    def htm_parse(self, priority, url, keys, deep, critical, parse_repeat, content):
        """
        parse the content of a url, you can rewrite this function, parameters and return refer to self.working()
        """

        cur_html = content

        # get url_list and save_list
        url_list = []    # 其他请求列表
        save_list = []   # 结果列表

        # return url_list, save_list
        return url_list, save_list
