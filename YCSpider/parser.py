# _*_ coding: utf-8 _*_

import re
import random
import logging
import datetime


class Parser(object):
    """
    Parser,to parse html
    """

    def __init__(self):
        self.log_str_format = "priority=%s, keys=%s, deep=%s, critical=%s, parse_repeat=%s, url=%s"
        return

    def working(self, url, content):
        try:
            url_list, save_list = self.htm_parse(content)
        except Exception as excep:
            # 重试
            url_list = []
            save_list = []

        return url_list, save_list

    def htm_parse(self, content):

        cur_html = content

        # 获得 url_list && save_list
        url_list = []  # 其他请求列表
        save_list = []  # 结果列表

        # 解析下一页请求的地址列表
        u_pattern = re.compile('')
        u_list = re.findall(u_pattern, cur_html, flags=re.IGNORECASE)
        for each in u_list:
            url_list.append(each)

        # 解析当前页具体数据结果
        s_pattern = re.compile('')
        s_list = re.findall(s_pattern, cur_html, flags=re.IGNORECASE)
        for each in s_list:
            save_list.append(each)

        return url_list, save_list
