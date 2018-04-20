# coding=gbk
import time
from lxml import html
import os
import requests
from chardet import detect
from bs4 import BeautifulSoup
import json

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

headers2 = {
    'Host': 'feed.mix.sina.com.cn',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Connection': 'keep-alive',
    # 'Accept-Encoding': 'gzip, deflate',
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
}

def save(text, filename='temp', path='download'):
    fpath = os.path.join(path, filename)
    with open(fpath, 'wb') as f:
        print('output:', fpath)
        f.write(text)

def save_image(path, image_url):
    resp = requests.get(image_url)
    page = resp.content
    filename = image_url.split('/')[-1]
    if '?' in filename:
        filename = filename.split('?')[0]
    save(page, filename, path)

def crawl(url):
    resp = requests.get(url, headers = headers)
    page = resp.content

    soup = BeautifulSoup(page, 'lxml', from_encoding='utf-8')
    # 获取文件名
    title_class = soup.select(".main-title")
    if title_class:
        title = title_class[0].string
    else:
        title = soup.select("#artibodyTitle")[0].string

    path = 'download\\' + title
    isEx = os.path.exists(path)
    if not isEx:
        os.makedirs(path)

    for imgs in soup.find_all("div", class_="img_wrapper"):
        for img in imgs.find_all("img"):
            # print(img.get("src"))
            save_image(path, img.get("src"))
    fpath = os.path.join(path, title + '.txt')
    with open(fpath, 'w') as f:
        for p_cons in soup.find_all("div", id="artibody"):
            for p_con in p_cons.find_all("p"):
                spans = p_con.find_all("span")
                if spans:
                    content = p_con.find_all("span")[0].string
                    # print p_con.contents[0]
                else:
                    content = p_con.string
                print(content)
                if content is not None:
                    f.write(content.encode("utf-8") + "\n")
    f.close()


def crawl_home(url):
    resp = requests.get(url, headers = headers)
    page = resp.content
    soup = BeautifulSoup(page, 'lxml', from_encoding='utf-8')
    # print(soup.prettify())
    # return
    url_set = set()
    # for link in soup.select('a[href*="doc-"]'):
    #     href = link.get("href")
    #     print href
    #     if href in url_set:
    #         continue
    #     crawl(link.get("href"))
    #     url_set.add(href)

    # 另外一部分信息需要通过接口获取
    # http://feed.mix.sina.com.cn/api/roll/get?pageid=434&lid=2666&num=10&versionNumber=1.2.4&page=2&encode=utf-8&_=1524216930272
    news_list_url = "http://feed.mix.sina.com.cn/api/roll/get?pageid=434&lid=2666&num=10&versionNumber=1.2.4&page=2&encode=utf-8&_=1524216930272"
    json_con = requests.get(news_list_url, headers=headers2).content
    # json_str = json.dump(json_con)
    data = json.loads(json_con)
    if data:
        for link_obj in data.result.data:
            print(link_obj.url)

if __name__ == '__main__':
    # url = 'http://finance.sina.com.cn/blockchain/coin/2018-04-19/doc-ifzihnep9257549.shtml'
    url = 'http://finance.sina.com.cn/blockchain/'
    crawl_home(url)