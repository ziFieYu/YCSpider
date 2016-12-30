# -*- coding: utf-8 -*-

'''
配置文件
'''

configs = {
    'redis': {
        'host': '192.168.130.125',
        'port': 6379,
        'urls_key': '%s:start_urls',
        'item_key': '%s:item'
    },
    'crawl': {
        'download_num': 10,
        'parser_num': 2,
        'saver_num': 1,
    }
}
