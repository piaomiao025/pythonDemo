#coding=utf-8
import os
from bs4 import BeautifulSoup
import requests

# name = u'download\\"\u6d88\u8d39/\u6c7d\u8f66/\u4f9b\u5e94\u94fe\u91d1\u878d"\u8ba8\u8bba:\u9648\u6653\u534e&\u738b\u6668\u6656&\u5f90\u5efa\u521a'
# name = name.replace(":", " ")
# name = name.replace("\"", "")
# name = name.replace("/", "-")
# print name.encode("utf-8")

# title = "“野蛮人”进军数字货币市场 创业者面临多重挑战|区块链_新浪财经_新浪网"
# print title[0: title.rfind('|')]

headers = {
    'Host': 'finance.sina.com.cn',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Connection': 'keep-alive',
    # 'Accept-Encoding': 'gzip, deflate',
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
}
url = "http://finance.sina.com.cn/blockchain/coin/2018-04-23/doc-ifzqvvrz9385640.shtml"
# url = "http://www.runoob.com/mongodb/mongodb-connections.html"
resp = requests.get(url, headers=headers)
soup = BeautifulSoup(resp.content, "lxml")
tags = soup.find_all('meta', attrs={'name':'tags'})
keywords = soup.find_all('meta', attrs={'name':'keywords'})
description = soup.find_all('meta', attrs={'name':'description'})
if tags:
    print("tags:" + tags[0]['content'])
if keywords:
    print("keywords:" + keywords[0]['content'])