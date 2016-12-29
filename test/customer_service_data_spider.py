# -*- coding: utf-8 -*-
import re
import sys
import requests
import xlsxwriter
import codecs

reload(sys)
sys.setdefaultencoding('utf-8')


class CustomerServiceDataSpider(object):
    def __init__(self):
        self.host = 'http://192.168.200.103:18080/EliteKM/newpages/'
        self.host_content = 'http://192.168.200.103:18080'
        self.start_url = 'http://192.168.200.103:18080/EliteKM/newpages/shownodechilds.jsp?node_a_id=16032104315'
        self.pattern_replace = '<[^>]*?>'
        self.decoder = codecs.getdecoder('utf_16_le')

    def crawl(self):
        result = []
        home_pattern = '<li class=".*?">[\s\S]*?<a href="(?P<url>.*?)" title="(?P<title>.*?)"'
        title_1 = '钱宝网知识库'
        html_home_response = self.get_response(self.start_url)
        html_home = str(html_home_response.text)
        home_list = re.findall(home_pattern, html_home)
        g1 = 0
        for each in home_list:
            g1 += 1
            # if g1 > 1:
            #     break
            # if g1 != 1:
            #     continue
            title_2 = str(each[1])
            url_2 = self.host + str(each[0])
            html_2_response = self.get_response(url_2)
            html_2 = str(html_2_response.text)
            list_2 = re.findall(home_pattern, html_2)
            g2 = 0
            for each2 in list_2:
                g2 += 1
                title_3 = str(each2[1])
                url_3 = self.host + str(each2[0])
                html_3_response = self.get_response(url_3)
                html_3 = str(html_3_response.text)
                list_3 = re.findall(home_pattern, html_3)
                tt1 = str(g1) + '/' + str(len(home_list))
                tt2 = str(g2) + '/' + str(len(list_2))
                if len(list_3) == 0:
                    title_4 = ''
                    title_5 = ''
                    title_6 = ''
                    # print title_1, title_2, title_3, title_4, title_5, title_6
                    content = self.get_content(html_3)
                    result.append((title_1, title_2, title_3, title_4, title_5, title_6, content))
                else:
                    for each3 in list_3:
                        title_4 = str(each3[1])
                        url_4 = self.host + str(each3[0])
                        html_4_response = self.get_response(url_4)
                        html_4 = str(html_4_response.text)
                        list_4 = re.findall(home_pattern, html_4)
                        if len(list_4) == 0:
                            title_5 = ''
                            title_6 = ''
                            print '正在采集：', len(result), tt1, tt2, title_1, title_2, title_3, title_4, len(list_4)
                            content = self.get_content(html_4)
                            result.append((title_1, title_2, title_3, title_4, title_5, title_6, content))
                        else:
                            for each4 in list_4:
                                title_5 = str(each4[1])
                                url_5 = self.host + str(each4[0])
                                html_5_response = self.get_response(url_5)
                                html_5 = str(html_5_response.text)
                                list_5 = re.findall(home_pattern, html_5)
                                if len(list_5) == 0:
                                    title_6 = ''
                                    print '正在采集：', len(result), tt1, tt2, title_1, title_2, title_3, title_4, len(
                                        list_5)
                                    content = self.get_content(html_5)
                                    result.append((title_1, title_2, title_3, title_4, title_5, title_6, content))
                                else:
                                    for each5 in list_5:
                                        title_6 = str(each5[1])
                                        print '正在采集：', len(result), tt1, tt2, title_1, title_2, title_3, title_4, 0
                                        url_6 = self.host + str(each5[0])
                                        html_6_response = self.get_response(url_6)
                                        html_6 = str(html_6_response.text)
                                        content = self.get_content(html_6)
                                        result.append((title_1, title_2, title_3, title_4, title_5, title_6, content))
        return result

    def savedata(self, result, filename):
        workbook = xlsxwriter.Workbook(unicode(str(filename) + '.xlsx'))
        worksheet = workbook.add_worksheet()
        worksheet.write(0, 0, unicode('标题1'))
        worksheet.write(0, 1, unicode('标题2'))
        worksheet.write(0, 2, unicode('标题3'))
        worksheet.write(0, 3, unicode('标题4'))
        worksheet.write(0, 4, unicode('标题5'))
        worksheet.write(0, 5, unicode('标题6'))
        worksheet.write(0, 6, unicode('内容'))
        index_row = 0
        for each_row in result:
            index_row += 1
            index_col = -1
            for each_col in each_row:
                try:
                    index_col += 1
                    try:
                        worksheet.write(index_row, index_col, unicode(each_col))
                    except:
                        print '*' * 50
                        # print index_col, index_row[0], index_row[1], index_row[2], index_row[3], index_row[4], \
                        #     index_row[5]
                except:
                    pass
        workbook.close()

    def get_content(self, html):
        pattern_content_url = '<IFRAME ID=.*?SRC="(?P<url>.*?)"'
        pattern_content = '<body[\s\S]*?</body>'
        content = ''
        url_content = re.search(pattern_content_url, html)
        if url_content:
            url_content = self.host_content + str(url_content.group('url'))
            html_content_response = self.get_response(url_content)
            if '<frameset rows' not in html_content_response.text:
                try:
                    html_content = str(html_content_response.content).decode('gbk').encode('utf-8')
                except:
                    try:
                        html_content = str(self.decoder(html_content_response.content)[0])
                    except:
                        html_content = str(html_content_response.content)
                content = re.search(pattern_content, html_content)
                if content:
                    content = content.group()
                    content = re.sub(self.pattern_replace, '', content)
                    content = content.replace('&nbsp;', ' ')
                else:
                    print '- ' * 10
            else:
                print '- ' * 10
        else:
            print '- ' * 10
        return content

    def get_response(self, url):
        return requests.get(url)

    def test(self):
        pattern_content_url = '<IFRAME ID=.*?SRC="(?P<url>.*?)"'
        pattern_content = '<body[\s\S]*?</body>'
        url = 'http://192.168.200.103:18080/EliteKM/newpages/loadarticle.jsp?ARTICLE_A_ID=3F21A816-97BF-7347-AAD4-FEDB8DA3EAAA'
        r = self.get_response(url)
        html = str(r.content).decode('gbk').encode('utf-8')
        url_content = re.search(pattern_content_url, html)
        if url_content:
            url_content = self.host_content + str(url_content.group('url'))
            print url_content
            html_content_response = self.get_response(url_content)
            if '<frameset rows' not in html_content_response.text:
                # html_content = str(self.decoder(html_content_response.content)[0])
                # html_content = str(html_content_response.content).decode('gbk').encode('utf-8')
                html_content = str(html_content_response.content)
                # content = re.search(pattern_content, html_content)
                print html_content
            else:
                print '000000'
        else:
            print '0'

    def test2(self):
        filename = '测试'
        workbook = xlsxwriter.Workbook(unicode(filename + '.xlsx'))
        worksheet = workbook.add_worksheet()
        worksheet.write(1, 1, '你好')
        worksheet.write(1, 2, 'bbb')
        worksheet.write(1, 3, 'ccc')
        worksheet.write(2, 1, '111')
        worksheet.write(2, 2, '222')
        worksheet.write(2, 3, '333')
        workbook.close()


if __name__ == '__main__':
    csdSpider = CustomerServiceDataSpider()
    result = csdSpider.crawl()
    print '采集完成，共采集：', len(result)
    print '正在保存数据...'
    csdSpider.savedata(result, '钱宝网知识库')
