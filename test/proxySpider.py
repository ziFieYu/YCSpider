# -*- coding: utf-8 -*-
import re
import sys

import redis
import requests
import time

reload(sys)
sys.setdefaultencoding('utf-8')


class ProxySpider(object):
    def __init__(self):
        self.redisclient = redis.Redis('192.168.130.125', 6379)

    def crawl(self):
        pass
        # 快代理
        rediskey = 'proxy:kuaidaili'
        url = 'http://www.kuaidaili.com/free/inha/%d/'
        pattern = '"IP">(?P<ip>.*?)</td>[^>]*?"PORT">(?P<port>.*?)</td>'
        ip_list = self.get_proxy(url, pattern, rediskey=rediskey)

        # 西刺
        rediskey = 'proxy:xici'
        url = 'http://www.xicidaili.com/nn/%d'
        headers = {
            'Host': 'www.xicidaili.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, sdch'
        }
        pattern = '<tr class="odd">[^<]*?<.*?</td>[^<]*?<td>(?P<ip>.*?)</td>[^<]*?<td>(?P<port>.*?)</td>[\s\S]*?<td>(?P<sj>\d{2}-\d{2}-\d{2} \d{2}:\d{2})</td>'
        ip_list = self.get_proxy(url, pattern, rediskey=rediskey, headers=headers)

    def verify(self):
        proxy_list = self.redisclient.lrange('proxy:result', 0, -1)
        for proxy in proxy_list:
            if self.verify_proxy(proxy):
                self.redisclient.lpush('proxy:valid', proxy)
            else:
                print 'invalid', proxy

    def get_proxy(self, url, pattern, rediskey, headers=None, start_url='', start_page=1, end_page=100):
        result = []
        for page in range(start_page, end_page):
            try:
                if page == start_page:
                    url_proxy = start_url if start_url != '' else url % page
                else:
                    url_proxy = url % page
                time.sleep(3)
                r = requests.get(url_proxy, headers=headers, timeout=10)
                html = str(r.text)
                ip_list = re.findall(pattern, html)
                print len(ip_list), url_proxy
                for e in ip_list:
                    proxy_ip = str(e[0] + ':' + str(e[1]))
                    self.redisclient.lpush(rediskey, proxy_ip)
                    result.append(proxy_ip)
            except Exception as ex:
                print ex
        return result

    def verify_proxy(self, proxy):
        ipinfo = str(proxy).split(':')
        proxies = {
            "http": "http://%s" % proxy,
        }
        try:
            r = requests.get('http://1212.ip138.com/ic.asp', proxies=proxies, timeout=10)
            html = str(r.text)
            if ipinfo[0] in html:
                return True
        except:
            pass


if __name__ == '__main__':
    ps = ProxySpider()
    # ps.crawl()
    # ps.verify()

    redisclient = redis.Redis('192.168.130.125', 6379)

    # proxy_valid2 = redisclient.lrange('proxy:valid_temp', 0, -1)
    # proxy_valid = redisclient.lrange('proxy:valid', 0, -1)
    # list_ok = []
    # list_error = []
    # for proxy in proxy_valid2:
    #     if proxy not in proxy_valid:
    #         if (ps.verify_proxy(proxy)):
    #             list_ok.append(proxy)
    #             redisclient.lpush('proxy:valid', proxy)
    #             print proxy
    #         else:
    #             list_error.append(proxy)
    #             # redisclient.lpush('proxy:error_1', proxy)
    # print 'OK', len(list_ok)
    # print 'NO OK', len(list_error)

    proxy_list = redisclient.lrange('proxy:valid', 0, -1)
    for proxy in proxy_list:
        try:
            proxies = {
                "http": "http://%s" % proxy,
            }
            r = requests.get('http://www.imeidb.com/', proxies=proxies, timeout=30)
            print r.status_code, proxy
        except:
            print 404, proxy
