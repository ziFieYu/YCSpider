# -*- coding: utf-8 -*-
import os
import re

import requests
import json
import logging
import time

import sys

reload(sys)
sys.setdefaultencoding('utf-8')


class TaoBaoLogin:
    """淘宝网登录"""

    def __init__(self, qr_file_path):
        logging.basicConfig(level=logging.WARNING,
                            format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S',
                            # filename='tbLogin.log',
                            filemode='w')
        self.qr_file_path = qr_file_path
        self.get_qr_code_url = 'https://qrlogin.taobao.com/qrcodelogin/generateQRCode4Login.do?adUrl=&adImage=&adText=&viewFd4PC=&viewFd4Mobile=&from=tbTop'
        self.get_qr_code_png_url = ''
        self.lgToken = ''
        self.adToken = ''
        self.get_scan_url = ''
        self.get_login_cookie_url = ''

    def get_qr_code(self):
        """获取淘宝登录二维码"""
        logging.warning('获取淘宝登录二维码')
        html = self.get_response(self.get_qr_code_url)[1]
        result = json.loads(html)
        imageurl = result.get('url', '')
        self.get_qr_code_png_url = 'https:' + str(imageurl) if imageurl else imageurl
        self.lgToken = str(result.get('lgToken', ''))
        self.adToken = result.get('adToken', '')
        self.get_scan_url = 'https://qrlogin.taobao.com/qrcodelogin/qrcodeLoginCheck.do?lgToken=' + self.lgToken
        self.get_scan_url += '&defaulturl=https%3A%2F%2Fwww.taobao.com%2F&_ksTS=1481614756915_1534&callback='
        ir = self.get_response(self.get_qr_code_png_url)
        if ir[0] == 200:
            open(self.qr_file_path, 'wb').write(ir[1])
            logging.warning('成功获取淘宝登录二维码，请扫描登录')
            os.system(self.qr_file_path)
            return True
        else:
            logging.error('下载二维码错误')
            return False

    def get_scan(self):
        """
        扫码登录
        :return: 1 成功；2登录成功；0 失败
        """
        r = 0
        while True:
            res = self.get_response(self.get_scan_url)
            if res[0] == 200:
                result = json.loads(res[1])
                code = int(result.get('code', 0))
                if code == 10004:
                    # 二维码有效期3分钟
                    logging.error('二维码失效')
                    break
                elif code == 10001:
                    logging.warning('扫描成功')
                    r = 1
                    time.sleep(2)
                elif code == 10006:
                    logging.warning('登录成功')
                    r = 2
                    self.get_login_cookie_url = result.get('url', '')
                    break
                time.sleep(3)
            else:
                logging.error('获取二维码扫描结果失败')
                break
        return r

    def get_login_cookie(self):
        """获取登陆后cookie"""
        headers = {
            'Host': 'login.taobao.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Referer': 'https://login.taobao.com/member/login.jhtml?redirectURL=https%3A%2F%2Fwww.taobao.com%2F',
            'Cookie': '_uab_collina=148159590013766250184744; t=bc9c21641f0396757e720a93f4c557b1; thw=cn; mt=np=&ci=1_1&cyk=0_0; cna=QHOxEL3sLjACAXT3f8qaTlgw; l=AvDw6VMsfL9HhVnVrjK0a2xIwLRDJNSC; isg=AgcHagM7E86HzZdUTMPO0Hall7spSdvuNMJrYdn1Pha8SCMK4dhDPrRCnJP7; _umdata=A502B1276E6D5FEF03A91837E6F0FC2313F3DC96C3EA279B49C1E58788DE2ACF527E1B67190A74227063564BCF4F9BDBBCB5A5C7425C1BD4E23D79B331B733B9B479F010227CBEC03C747AB4573F7F2B1F5EB66C2D97806CD1EBB7D61C8041DA; uc3=sg2=UoZIQTPC6RhOAkupjRK7NxfAVfmg%2BBx4nVpYc2sJMRk%3D&nk2=rr9SYJ4%2FLj3C1A9NuKusUQ%3D%3D&id2=VASr1AOvTymX&vt3=F8dARHYsdoHy4KH2lUE%3D&lg2=VT5L2FSpMGV7TQ%3D%3D; lid=%E6%8C%96%E9%87%91%E8%B1%86%E8%B1%86%E7%9A%84%E5%B0%8F%E6%97%B7%E5%B7%A5; uss=UU6of5dBKDCgR0vYWCTXhiElHCxohnbPYOFNjTtE5RwFumfAYYst8AdqpA%3D%3D; tracknick=%5Cu6316%5Cu91D1%5Cu8C46%5Cu8C46%5Cu7684%5Cu5C0F%5Cu65F7%5Cu5DE5; _cc_=Vq8l%2BKCLiw%3D%3D; tg=0; lc=Vy7uhVo25ARZ4FlYr%2FA%2F6Zy%2FEx8k; x=e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0%26__ll%3D-1%26_ato%3D0; lgc=%5Cu6316%5Cu91D1%5Cu8C46%5Cu8C46%5Cu7684%5Cu5C0F%5Cu65F7%5Cu5DE5; v=0; cookie2=183691fba590479af0ac5377a51f2b04; _tb_token_=e51be36b3588e'
        }
        response = requests.get(self.get_login_cookie_url, headers=headers, allow_redirects=False)
        cookies = response.headers['Set-Cookie']
        return cookies

    def get_orders(self, cookies, page=1, toppage=0, sleep=5):
        """
        获取订单信息
        :param cookies: 登录后cookie
        :param page: 采集第几页订单
        :param toppage: 采集前几页订单
        :param sleep: 休眠时间
        :return: 生成器
        """
        url = 'https://buyertrade.taobao.com/trade/itemlist/asyncBought.htm?action=itemlist/BoughtQueryAction&event_submit_do_query=1&_input_charset=utf8'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Encoding': 'gzip, deflate, br',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Referer': 'https://buyertrade.taobao.com/trade/itemlist/list_bought_items.htm?spm=a21bo.50862.1997525045.2.LuBmK3',
            'Cookie': cookies
        }
        while True:
            if toppage != 0 and page > toppage:
                break
            aa = 'pageNum=' + str(page)
            aa += '&pageSize=15&action=itemlist%2FBoughtQueryAction&prePageNo=2&buyerNick=&dateBegin=0&dateEnd=0&lastStartRow=&logisticsService=&options=0&orderStatus=&queryBizType=&queryOrder=desc&rateStatus=&refund=&sellerNick='
            page += 1
            time.sleep(sleep)
            r = requests.post(url, data=aa, headers=headers)
            orders = json.loads(r.text)['mainOrders']
            if orders:
                for each in orders:
                    order_id = each.get('id', '')
                    create_time = each['orderInfo'].get('createTime', '')
                    shop_name = each.get('seller', '')
                    shop_name = shop_name.get('shopName', '') if shop_name else ''
                    goods_title = each['subOrders'][0]['itemInfo'].get('title', '')
                    price = each['subOrders'][0]['priceInfo'].get('realTotal', '')
                    goods_num = each['subOrders'][0].get('quantity', '')
                    pay_price = each['payInfo'].get('actualFee', '')
                    goods_status = each['statusInfo'].get('text', '')
                    yield (order_id, create_time, shop_name, goods_title, price, goods_num, pay_price, goods_status)
            else:
                break

    def send_wangwang_msg(self, cookies, loginTag='69B87BEBCC88BC487', sendmsg='测试', userId='yun809195246'):
        print 'cookies:', cookies
        cookie2 = re.search('(?<=cookie2=).*?(?=;)', cookies).group()
        print 'cookie2:', cookie2
        username = re.search('(?<=lid=).*?(?=;)', cookies).group()
        print 'username:', username

        headers = {
            'Host': 'webww.taobao.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0',
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Referer': 'https://buyertrade.taobao.com/trade/itemlist/list_bought_items.htm?spm=a21bo.50862.1997525045.2.kdt5KG',
            'Cookie': cookies
        }

        while True:
            print '-' * 50
            # 登录旺旺
            url = 'https://webww.taobao.com/login.do?token=' + cookie2 + '&callback=TDog.WebServer.prepareLogin&nickName='
            url += username + '&autoLogin=1&loginTag=' + loginTag + '&nkh=' + username + '&appId=24&t='
            r = requests.get(url, headers=headers)
            print '开始登录', r.status_code, r.text

            # 退出旺旺客户端
            url = 'https://webww.taobao.com/login.do?token=' + cookie2
            url += '&callback=TDog.WebServer.prepareLogin&nickName=' + username
            url += '&autoLogin=3&loginTag=' + loginTag + '&nkh=' + username + '&appId=24&t='
            r = requests.get(url, headers=headers)
            print '退出旺旺客户端', r.status_code, r.text

            if '"success":"true"' in str(r.text):
                # 获取登录状态
                url = 'https://webww.taobao.com/getloginresult.do?time=1&token=' + cookie2
                url += '&callback=TDog.WebServer.disposeLoginResult&nkh=' + username + '&appId=24&t='
                r = requests.get(url, headers=headers)
                print '获取登录结果', r.status_code, r.text
                if '"success":"true"' in str(r.text):
                    break
            time.sleep(5)
        # 发送信息
        sendUrl = 'https://webww.taobao.com/send.do?token=' + cookie2
        sendUrl += '&callback=TDog.WebServer.handleSendResult&userId=cntaobao' + userId
        sendUrl += '&content=' + sendmsg + '&nkh=' + username + '&appId=24&t='
        r = requests.get(sendUrl, headers=headers)
        print r.status_code
        print r.text

    def get_response(self, url):
        response = requests.get(url)
        return response.status_code, response.content, response


if __name__ == '__main__':
    tbLogin = TaoBaoLogin('a.png')
    while True:
        if tbLogin.get_qr_code():
            time.sleep(1)
            result = tbLogin.get_scan()
            if result:
                break
            print '重新获取二维码'
            time.sleep(1)
    cookies = tbLogin.get_login_cookie()
    while True:
        print ''
        print ''
        print '    操作说明'
        print '  --------------------'
        print '  | 获取 订单列表 请输入: 1'
        print '  | 获取 个人资料 请输入: 2'
        print '  | 获取 收货地址 请输入: 3'
        print '  --------------------'
        _input = raw_input("请输入操作选项：")
        if _input == '1':
            # 获取订单
            orders = tbLogin.get_orders(cookies)
            order_total = 0
            for each in orders:
                order_total += 1
                msg = u'订单号：%s | 购买时间：%s | 店铺：%s | 商品标题：%s | 价格：%s | 数量：%s | 实付款：%s | 交易状态：%s'
                print msg % each
            print u'共%d条订单数据' % order_total
        elif _input == '0':
            # 登录阿里旺旺 69B87BEBCC88BC487
            print '登录阿里旺旺'
            loginTag = raw_input("请输入loginTag：")
            if loginTag == '':
                loginTag = '69B87BEBCC88BC487'
            print 'loginTag:', loginTag
            tbLogin.send_wangwang_msg(cookies, loginTag=loginTag)
