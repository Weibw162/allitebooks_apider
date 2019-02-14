import requests
import random
from lxml import etree
import json


class Allitebooks_apider(object):

    def __init__(self):
        self.url = "http://www.allitebooks.com/"
        self.book_info_list=[]

    def get_headers(self):
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

    def get_response(self):
        proxies = {
            "http": "http://59.108.125.241:8080",
            "http": "http://125.118.173.26:9999",
            "http": "http://124.128.76.142:8060",
            "http": "http://223.85.196.75:9999",
            "http": "http://123.161.21.32:9797",

        }



        response = requests.get(self.url,headers=self.get_headers(),proxies=proxies,timeout=2).content.decode("utf-8")
        print("开始获取HTML信息")
        return response

    def get_parse_xpath_booklist(self,response):
        html = etree.HTML(response)
        book_list = html.xpath('//div[@class="main-content-inner clearfix"]/article')
        print("解析获取booklist")
        return book_list

    def get_parse_xpath_onebook(self,book_list):
        for book in book_list:
            book_info = {}
            book_info["book_name"] = book.xpath('.//h2[@class="entry-title"]/a/text()')[0]
            book_info["book_author"] = book.xpath('.//span[@class="author vcard"]/h5/a/text()')[0] if len(book.xpath('.//span[@class="author vcard"]/h5/a/text()')) == 1 else book.xpath('.//span[@class="author vcard"]/h5/a/text()')
            book_info["book_info"] = book.xpath('.//div[@class="entry-summary"]/p/text()')[0]
            book_info["book_img_url"] = book.xpath('.//div[@class="entry-thumbnail hover-thumb"]/a/img/@src')[0]
            book_info["book_info_url"] = book.xpath('.//div[@class="entry-thumbnail hover-thumb"]/a/@href')[0]
            # print(book_author)
            self.book_info_list.append(book_info)
        return self.book_info_list

    def save_data(self,data):
        book_data = json.dump(data,open('book_info.json','w'))

    def run(self):
        response = self.get_response()
        book_list = self.get_parse_xpath_booklist(response)
        # print(book_list)
        data = self.get_parse_xpath_onebook(book_list)
        self.save_data(data)
Allitebooks_apider().run()
