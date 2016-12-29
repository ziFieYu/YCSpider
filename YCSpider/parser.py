# _*_ coding: utf-8 _*_

import re
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

class Parser(object):
    """
    解析器
    """

    def working(self, url, meta, response):
        code = 1
        try:
            url_list, save_list = self.htm_parse(url, meta, response)
        except Exception as excep:
            url_list, save_list = [], []
            code = -1  # 重试

        return code, url_list, save_list

    def htm_parse(self, url, meta, response):
        # content = (url, response)
        cur_html = response.text

        # 获得 url_list && save_list
        url_list = []
        save_list = []

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
