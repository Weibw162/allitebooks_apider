import requests
import random
from lxml import etree
import json


class Taobao_spider(object):

    def __init__(self):

        """配置"""

        self.url = "http://www.allitebooks.com/"
        self.book_info_list=[]
        self.proxies = {
            "http": "http://59.108.125.241:8080",
            "http": "http://125.118.173.26:9999",
            "http": "http://124.128.76.142:8060",
            "http": "http://223.85.196.75:9999",
            "http": "http://123.161.21.32:9797",

        }

    def get_headers(self):

        """获取请求头"""

        headers_list = [
            "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.57.2 (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2",
            "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER",
        ]
        headers = {
            "User-Agent":random.choice(headers_list)
        }
        return headers


    def get_book_type_response(self):

        """获取网页主页的信息"""

        print("正在获取网页信息")
        status_code = 1
        while status_code != 200:
            try:
                book_type_response = requests.get(self.url, headers=self.get_headers(), proxies=self.proxies).content.decode("utf-8")
                status_code = 200
            except ConnectionError:
                print("第{}次请求失败".format(status_code))
                status_code += 1

        print("网页信息获取成功")
        return book_type_response

    def get_book_type_url(self,book_type_response):

        """解析获取书籍种类"""

        print("开始获取种类")
        book_type_data = etree.HTML(book_type_response)
        book_type_url_list = book_type_data.xpath('//div[@class="hfeed site"]//section[@class="content-area"]//ul/li')
        print("种类获取成功")
        return book_type_url_list

    def get_book_type_info(self,book_type_url_list):

        """解析获取书籍种类详细信息：种类名及链接"""

        print("开始解析信息，获取书籍种类名及链接")
        book_type_info_list = []
        for book_type in book_type_url_list:
            book_type_info_dict = {}
            book_type_info_dict["book_type_name"] = book_type.xpath('./a/text()')[0]
            book_type_info_dict["book_type_url"] = book_type.xpath('./a/@href')[0]
            book_type_info_list.append(book_type_info_dict)
        print("解析完毕")
        return book_type_info_list


    def get_onetype_response(self,book_onetype_url):

        """获取单个种类书籍的首页信息"""

        print("开始获取{}的HTML信息".format(book_onetype_url))
        status_code = 1
        while status_code != 200:
            try:
                onetype_response = requests.get(book_onetype_url, headers=self.get_headers(), proxies=self.proxies).content.decode(
                    "utf-8")
                status_code = 200
            except ConnectionError:
                print("第{}次请求失败".format(status_code))
                status_code += 1
        print("获取成功")
        return onetype_response

    def get_parse_xpath_booklist(self, onetype_response):

        """解析获取书籍列表"""

        print("解析获取booklist")
        html = etree.HTML(onetype_response)
        book_list = html.xpath('//div[@class="main-content-inner clearfix"]/article')
        print("解析成功")
        return book_list

    def get_parse_xpath_onebook(self,book_list):

        """解析获取每本书的信息：书名，作者，简介，图地址，详细信息地址"""

        print("开始解析详细信息")
        for book in book_list:
            book_info = {}
            book_info["book_name"] = book.xpath('.//h2[@class="entry-title"]/a/text()')[0]
            book_info["book_author"] = book.xpath('.//span[@class="author vcard"]/h5/a/text()')[0] if len(book.xpath('.//span[@class="author vcard"]/h5/a/text()')) == 1 else book.xpath('.//span[@class="author vcard"]/h5/a/text()')
            book_info["book_info"] = book.xpath('.//div[@class="entry-summary"]/p/text()')[0]
            book_info["book_img_url"] = book.xpath('.//div[@class="entry-thumbnail hover-thumb"]/a/img/@src')[0]
            book_info["book_info_url"] = book.xpath('.//div[@class="entry-thumbnail hover-thumb"]/a/@href')[0]
            self.book_info_list.append(book_info)
            print("添加{}信息成功".format(book_info["book_name"]))
        print("本类书籍信息解析完毕")
        # print(self.book_info_list)
        return self.book_info_list


    def get_onebook_page_response(self,url):

        """获取一本书的详细信息 """

        print("开始获取{}页面信息".format(url))

        status_code = 1
        while status_code != 200:
            try:
                onebook_page_response = requests.get(url, headers=self.get_headers(),
                                                proxies=self.proxies).content.decode(
                    "utf-8")
                status_code = 200
            except ConnectionError:
                print("第{}次请求失败".format(status_code))
                status_code +=1

        print("获取成功")
        return onebook_page_response


    def get_parse_onebook_page(self,response):

        """解析每个详细页面的信息"""

        onebook_info= etree.HTML(response)
        onebook_info_dict = {}
        onebook_info_dict["ISBN-10"] = onebook_info.xpath('//div[@class="site-content clearfix"]//section[@class="content-area"]//header[@class="entry-header"]//div[@class="book-detail"]/dl/dd[2]/text()')[0]
        onebook_info_dict["Year"] = onebook_info.xpath(
            '//div[@class="site-content clearfix"]//section[@class="content-area"]//header[@class="entry-header"]//div[@class="book-detail"]/dl/dd[3]/text()')[0]
        onebook_info_dict["Pages"] = onebook_info.xpath(
            '//div[@class="site-content clearfix"]//section[@class="content-area"]//header[@class="entry-header"]//div[@class="book-detail"]/dl/dd[4]/text()')[0]
        onebook_info_dict["Language"] = onebook_info.xpath(
            '//div[@class="site-content clearfix"]//section[@class="content-area"]//header[@class="entry-header"]//div[@class="book-detail"]/dl/dd[5]/text()')[0]
        onebook_info_dict["File size"] = onebook_info.xpath(
            '//div[@class="site-content clearfix"]//section[@class="content-area"]//header[@class="entry-header"]//div[@class="book-detail"]/dl/dd[6]/text()')[0]
        onebook_info_dict["File format"] = onebook_info.xpath(
            '//div[@class="site-content clearfix"]//section[@class="content-area"]//header[@class="entry-header"]//div[@class="book-detail"]/dl/dd[7]/text()')

        return onebook_info_dict


    def save_data(self,data):

        """保存数据"""

        print("开始保存数据")
        json.dump(data,open('book_info3.json','w'))
        print("数据保存完毕")

    def run(self):

        """运行"""

        book_type_response = self.get_book_type_response()
        book_type_url_list = self.get_book_type_url(book_type_response)
        book_type_info_list = self.get_book_type_info(book_type_url_list)
        # print(book_type_info_list)
        for book_type_info in book_type_info_list:
            onetype_response = self.get_onetype_response(book_type_info["book_type_url"])
            book_list = self.get_parse_xpath_booklist(onetype_response)
            book_type_info["books"] = self.get_parse_xpath_onebook(book_list)

            for book_info_page in self.book_info_list:
                book_info_page_url = book_info_page["book_info_url"]
                book_info_page_respons = self.get_onebook_page_response(book_info_page_url)
                onebook_info_dict = self.get_parse_onebook_page(book_info_page_respons)
                book_info_page["info"] = onebook_info_dict

            self.book_info_list = []

        self.save_data(book_type_info_list)

Taobao_spider().run()
