# -*- encoding: utf-8 -*-
import json
import re

import requests

# r = requests.get(
#     'https://aldh5.tmall.com/recommend2.htm?notNeedBackup=true&appId=2016022921,201603018,2016030725,2016030726,2016031451,2016031452,2016031453,2016031454,2016031455,2016031456,2016031457,2016031458,2016030724&callback=jsonp_51349692')
#
# print r.text
# import redis
#
# client = redis.Redis('192.168.130.125', 6379)
# print client.rpop('urlSpider:items2')

# url = 'https://buyertrade.taobao.com/trade/itemlist/asyncBought.htm?action=itemlist/BoughtQueryAction&event_submit_do_query=1&_input_charset=utf8'
#
# headers = {
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0',
#     'Accept': 'application/json, text/javascript, */*; q=0.01',
#     'Accept-Encoding': 'gzip, deflate, br',
#     'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
#     'Referer': 'https://buyertrade.taobao.com/trade/itemlist/list_bought_items.htm?spm=a21bo.50862.1997525045.2.LuBmK3',
#     'Cookie': 'swfstore=306848; miid=174507073007555794; thw=cn; cna=VJKsEMaJqncCAXT3f8q05Ao7; uc2=wuf=https%3A%2F%2Ftrade.tmall.com%2Fdetail%2ForderDetail.htm%3Fbiz_order_id%3D2859751635129101%26forward_action%3D; hng=CN%7Czh-cn%7CCNY; _tb_token_=33b336b83f85; v=0; uc1=cookie14=UoW%2FXGmZjfGYFw%3D%3D&lng=zh_CN&cookie16=Vq8l%2BKCLySLZMFWHxqs8fwqnEw%3D%3D&existShop=false&cookie21=V32FPkk%2FgPzW&tag=7&cookie15=VFC%2FuZ9ayeYq2g%3D%3D&pas=0; uc3=sg2=UoZIQTPC6RhOAkupjRK7NxfAVfmg%2BBx4nVpYc2sJMRk%3D&nk2=rr9SYJ4%2FLj3C1A9NuKusUQ%3D%3D&id2=VASr1AOvTymX&vt3=F8dARHYsfdM1ELYsQME%3D&lg2=UtASsssmOIJ0bQ%3D%3D; existShop=MTQ4MTY5ODQ4MA%3D%3D; uss=UNRjXewKvCRJ3bZuP7L4gg86uulqkHFdkn%2BWMyF8XtSr6cHtGZ8e%2BpzXpw%3D%3D; lgc=%5Cu6316%5Cu91D1%5Cu8C46%5Cu8C46%5Cu7684%5Cu5C0F%5Cu65F7%5Cu5DE5; tracknick=%5Cu6316%5Cu91D1%5Cu8C46%5Cu8C46%5Cu7684%5Cu5C0F%5Cu65F7%5Cu5DE5; cookie2=1cc69d53791c563a731bf2f79065fd61; sg=%E5%B7%A510; mt=np=&ci=1_1&cyk=0_0; cookie1=BqfX6fMx%2F%2BUIy37Vj3jZflIAwpT%2BpYOAzJqNUiJila0%3D; unb=751050191; skt=f574b3ddf369234d; t=07bd247526f2d3693c616e1afd0fb70a; publishItemObj=Ng%3D%3D; _cc_=VT5L2FSpdA%3D%3D; tg=0; _l_g_=Ug%3D%3D; _nk_=%5Cu6316%5Cu91D1%5Cu8C46%5Cu8C46%5Cu7684%5Cu5C0F%5Cu65F7%5Cu5DE5; cookie17=VASr1AOvTymX; x=e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0%26__ll%3D-1%26_ato%3D0; ubn=p; ucn=center; whl=-1%260%260%261481700783762; l=Ap-fu3oIpDAmmwhKauLzLnBAr/k0QPMr; isg=At7efZIRClmRY17LB3LFkQcVL3ScUGmQW2MdA4h6DiGRq2CF9CuDKaYN1QBd'
# }
#
# aa = 'pageNum=1&pageSize=15&action=itemlist%2FBoughtQueryAction&prePageNo=2&buyerNick=&dateBegin=0&dateEnd=0&lastStartRow=&logisticsService=&options=0&orderStatus=&queryBizType=&queryOrder=desc&rateStatus=&refund=&sellerNick='
# r = requests.post(url, data=aa, headers=headers)
# print r.text
#
# r = requests.get('https://i.taobao.com/user/baseInfoSet.htm?spm=0.0.a210b.0.Z52XoM&tracelog=snsmytaobaoshezhi2ed',
#                  headers=headers)
# print r.text

# orders = aaa()
# if orders:
#     for each in orders:
#         msg = u'订单号：%s | 购买时间：%s | 店铺：%s | 商品标题：%s | 价格：%s | 数量：%s | 实付款：%s | 交易状态：%s'
#         print msg % each


# f = requests.get('http://img.alicdn.com/bao/uploaded/i8/TB11tBuNXXXXXboaXXXYXGcGpXX_M2.SS2', stream=True)
# print type(f.content)
# # print f.content

# cookies = 't=bc9c21641f0396757e720a93f4c557b1; thw=cn; mt=ci=1_1&cyk=0_0; cna=QHOxEL3sLjACAXT3f8qaTlgw; l=AqCgGXyOzK839QnF/qLEeH1-cKRycYRz; isg=Avb2GALIshI_sEbjFajPX3_ORiz1inXUjXlatmDfOll0o5U9yKNmYdBVzeQi; uc3=sg2=UoZIQTPC6RhOAkupjRK7NxfAVfmg%2BBx4nVpYc2sJMRk%3D&nk2=EEoq59phWpNZ0dHq1lW1&id2=WvKRCx3MHiSZ&vt3=F8dARHYqRCXjC9HK7zw%3D&lg2=UtASsssmOIJ0bQ%3D%3D; tracknick=stuartalexander; _cc_=U%2BGCWk%2F7og%3D%3D; tg=0; x=e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0%26__ll%3D-1%26_ato%3D0; uss=U7GhoPP9bDyTJtBcUAdg4vbQ6XwJqvmO%2F%2B6fLI4zXDvSfq%2BByx%2F5SJNhHA%3D%3D; cookie2=1dc8da496ad3001c701ad04e0dbe4c20; _tb_token_=fee4be3557be3; v=0; uc1=cookie14=UoW%2FXGdh7ARgww%3D%3D&lng=zh_CN&cookie16=WqG3DMC9UpAPBHGz5QBErFxlCA%3D%3D&existShop=false&cookie21=U%2BGCWk%2F7pY%2FF&tag=7&cookie15=UIHiLt3xD8xYTw%3D%3D&pas=0; existShop=MTQ4MTg2ODEzNQ%3D%3D; lgc=stuartalexander; sg=r8c; cookie1=U7U1ZkryvQCIkLQCRQeSSGYErnWXF2jQpkyLR1dJy38%3D; unb=926329058; skt=8341b88092c1cf3c; _l_g_=Ug%3D%3D; _nk_=stuartalexander; cookie17=WvKRCx3MHiSZ; whl=-1%260%260%261481868148411'
# headers = {
#     'Host': 'webww.taobao.com',
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0',
#     'Accept': '*/*',
#     'Accept-Encoding': 'gzip, deflate, br',
#     'Referer': 'https://buyertrade.taobao.com/trade/itemlist/list_bought_items.htm?spm=a1z02.1.1997525045.2.Zb8FGq&wwlight=cntaobao%E5%90%9B%E8%AF%9A%E9%9E%8B%E7%B1%BB%E4%B8%93%E8%90%A5%E5%BA%97',
#     'Cookie': cookies
# }


# 登录
# sendUrl = 'https://webww.taobao.com/login.do?token=1c09b111669062f9d22bb1462a06589f&callback=TDog.WebServer.prepareLogin&nickName=挖金豆豆的小旷工&autoLogin=1&loginTag=&nkh=挖金豆豆的小旷工&appId=24&t='
# r = requests.get(sendUrl, headers=headers)
# print '开始登录', r.status_code, r.text
#
# # 退出客户端
# sendUrl = 'https://webww.taobao.com/login.do?token=1c09b111669062f9d22bb1462a06589f&callback=TDog.WebServer.prepareLogin&nickName=挖金豆豆的小旷工&autoLogin=3&loginTag=&nkh=挖金豆豆的小旷工&appId=24&t='
# r = requests.get(sendUrl, headers=headers)
# print  '退出客户端', r.status_code, r.text
#
# # 获取登录结果
# sendUrl = 'https://webww.taobao.com/getloginresult.do?time=1&token=1c09b111669062f9d22bb1462a06589f&callback=TDog.WebServer.disposeLoginResult&nkh=挖金豆豆的小旷工&appId=24&t='
# r = requests.get(sendUrl, headers=headers)
# print '获取登录结果', r.status_code, r.text

# 发送信息
# sendUrl = 'https://webww.taobao.com/send.do?token=1c09b111669062f9d22bb1462a06589f&callback=TDog.WebServer.handleSendResult&userId=cntaobaostuartalexander&content=3&nkh=挖金豆豆的小旷工&appId=24&t='#
# r = requests.get(sendUrl, headers=headers)
# print r.status_code
# print r.text



# sendUrl = 'https://webww.taobao.com/tagkey.do?token=1dc8da496ad3001c701ad04e0dbe4c20&callback=TDog.WebServer.handleLoginFirst&nkh=stuartalexander&appId=24&t='
# r = requests.get(sendUrl, headers=headers)
# print r.history
# print r.headers
# print r.status_code, r.text
# # https://webww.taobao.com/login.do?token=1dc8da496ad3001c701ad04e0dbe4c20&callback=TDog.WebServer.prepareLogin&nickName=stuartalexander&autoLogin=1&loginTag=u9B87BEBCC88BC487&nkh=stuartalexander&appId=24&t=1481868155533
# sendUrl = 'https://webww.taobao.com/login.do?token=1dc8da496ad3001c701ad04e0dbe4c20&callback=TDog.WebServer.prepareLogin&nickName=stuartalexander&autoLogin=1&loginTag=u9B87BEBCC88BC487&nkh=stuartalexander&appId=24&t=1481868155533'
# r = requests.get(sendUrl, headers=headers)
# print r.history
# print r.headers
# print r.status_code, r.text

a = '1'
assert a, 'empty'
