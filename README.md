# allitebooks_apider
爬取网址www.allitebooks.com


## version0

使用requests库爬取，xpath进行解析，存入json文件。  

headers从headers_list中随机抽取，代理proxies直接在免费代理网站上拷贝下来几个用。  

此版本主要爬取网站首页显示的十本书。  


## version1

本版本首先爬取首页显示的十五个书籍种类，然后爬取每个种类的前十本书。  


## version2

本版本继承上一版本，继续深入每本书的详情页，爬取每本书的详情信息。  





