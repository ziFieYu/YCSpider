# -*- coding: utf-8 -*-
import random
import re

import redis
import requests
import sys

import time

reload(sys)
sys.setdefaultencoding('utf-8')


class IMEISearch:
    """
    手机IMEI code 查询
    """

    def __init__(self):
        self.redisclient = redis.Redis('192.168.130.125', 6379)
        self.proxy_list = self.redisclient.lrange('proxy:valid', 0, -1)
        print len(self.proxy_list)
        self.proxy = self.proxy_list[0]

    def start(self):
        code_list = ['863151023743237', '863664000059021', '353627053517317', '862002000000516', '358027056727110',
                     '013140000424951', '356440042114841', '990002717989097', '860310026085292', '862949026929765',
                     '013028005770587', '863091024967148', '013186001256264', '011093002268698', '357403043690945',
                     '866723019683291', '013412008535041', '860670023396392', '865343020104152', '351521004992889', ]
        r = self.check(code_list)
        print '正常的有：', len(r[0])
        print '非正常的有：', len(r[1])
        print '未采集的有：', len(r[2])

    def check(self, code_list):
        list_ok = []
        list_error = []
        list_other = []
        print len(code_list)
        for code in code_list:
            result = self.get_info_for_IMEI(code)
            if result[0] == 1:
                list_ok.append(result[1])
            elif result[0] == -1:
                list_error.append(code)
            elif result[0] == 0:
                list_other.append(code)
            else:
                print code
        return list_ok, list_error, list_other

    def get_info_for_IMEI(self, code, depth=3):
        flag = 0
        code_info = None
        url = 'http://www.imeidb.com/?xp=cCgWq6VwVz&imei=%s' % code
        for i in range(0, depth):
            r = self.get_html_for_proxy(url)
            html = str(r.text) if r else ''
            if html != '' and '您已经查询了很多次，系统就要崩溃啦！不如明天再来查吧' not in html:
                if '我们无法识别您输入的IMEI码' in html:
                    # 错误的IMEI码
                    flag = -1
                else:
                    brand = re.search('手机品牌</th>[^>]*?>(?P<aa>.*?)<', html)
                    brand = brand.group('aa') if brand else ''
                    brand = self.replace_str(brand)
                    model = re.search('手机型号</th>[^>]*?>(?P<aa>.*?)<', html)
                    model = model.group('aa') if model else ''
                    model = self.replace_str(model)
                    desc = re.search('IMEIdb手机性能指数</th>[^>]*?>(?P<aa>.*?)<', html)
                    desc = desc.group('aa') if desc else ''
                    desc = self.replace_str(desc)
                    print '-' * 50
                    print 'brand:', brand
                    print 'model:', model
                    print 'desc:', desc
                    flag = 1
                    code_info = (code, brand, model, desc)
                break
            else:
                self.get_random()
                if i + 1 == depth:
                    # 您已经查询了很多次，系统就要崩溃啦！不如明天再来查吧
                    pass
        return flag, code_info

    def replace_str(self, result, str_list=['IMEIdb.com免费查询', 'IMEIdb', '暂未对该型号进行评分，敬请期待']):
        '''
        替换指定字符为空
        :param result: 被替换的字符串
        :param str_list: 要替换的
        :return: 返回替换后的结果
        '''
        if str(result) != '':
            for e in str_list:
                result = result.replace(e, '')
            result = result.strip()
        return result

    def get_html_for_proxy(self, url):
        r = None
        for i in range(1, 3):
            print '代理IP：', self.proxy
            proxies = {
                "http": "http://%s" % self.proxy,
            }
            try:
                r = requests.get(url, proxies=proxies, timeout=5)
                break
            except:
                time.sleep(0.5)
                self.get_random()
        return r

    def get_random(self):
        random_index = random.randint(0, len(self.proxy_list) - 1)
        self.proxy = self.proxy_list[random_index]


if __name__ == '__main__':
    code_list = ['863151023743237', '863664000059021', '353627053517317', '862002000000516', '358027056727110',
                 '013140000424951', '356440042114841', '990002717989097', '860310026085292', '862949026929765',
                 '013028005770587', '863091024967148', '013186001256264', '011093002268698', '357403043690945',
                 '866723019683291', '013412008535041', '860670023396392', '865343020104152', '351521004992889', ]
    imei = IMEISearch()
    r = imei.check(code_list)
    print '正常的有：', len(r[0])
    print '非正常的有：', len(r[1])
    print '未采集的有：', len(r[2])
    print '\r\n\r\n\r\n'
    print '正常的有：', len(r[0])
    for e in r[0]:
        print e
    print '非正常的有：', len(r[1])
    for e in r[1]:
        print e
    print '未采集的有：', len(r[2])
    for e in r[2]:
        print e
