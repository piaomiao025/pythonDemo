# coding=utf-8
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

headers_feeds = {
    'Host': 'feed.mix.sina.com.cn',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Connection': 'keep-alive',
    # 'Accept-Encoding': 'gzip, deflate',
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
}

params = {
    'pageid': 434,
    'lid': 2666,
    'num': 10,
    'versionNumber': '1.2.4',
    'page': 1,
    'encode': 'utf-8',
    '_': 1
}

url_set = set()

def save(text, filename='temp', path='download'):
    fpath = os.path.join(path, filename)
    with open(fpath, 'wb') as f:
        # print('output:', fpath)
        f.write(text)

def save_image(path, image_url):
    if not image_url:
        return
    resp = requests.get(image_url)
    page = resp.content
    filename = image_url.split('/')[-1]
    if '?' in filename:
        filename = filename.split('?')[0]
    save(page, filename, path)

def crawl(url):
    try:
        resp = requests.get(url, headers=headers)
    except BaseException:
        print("第一次失败，重试一次")
        resp = requests.get(url, headers=headers)

    page = resp.content

    soup = BeautifulSoup(page, 'lxml', from_encoding='utf-8')
    # 获取文件名
    title = soup.title.string
    title = title[0: title.rfind('|')]

    # title_class = soup.select(".main-title")
    # if title_class:
    #     title = title_class[0].string
    # else:
    #     title = soup.select("#artibodyTitle")[0].string

    # if title != "doc-ifysvpiq9310474.shtml":
    #     return
    # 替换特殊字符
    title = title.replace(":", " ")
    title = title.replace("\"", "")
    title = title.replace("\\", "")
    title = title.replace("/", "-")
    title = title.replace("*", "")
    title = title.replace("?", "")
    title = title.replace("<", "(")
    title = title.replace(">", ")")
    title = title.replace("|", " ")

    path = 'download\\' + title

    isEx = os.path.exists(path)
    if not isEx:
        os.makedirs(path)


    tags = soup.find_all('meta', attrs={'name':'tags'})
    keywords = soup.find_all('meta', attrs={'name':'keywords'})
    descriptions = soup.find_all('meta', attrs={'name':'description'})
    if tags:
        tags = tags[0]['content']
    if keywords:
        keywords = keywords[0]['content']
    if descriptions:
        descriptions = descriptions[0]['content']

    for imgs in soup.find_all("div", class_="img_wrapper"):
        for img in imgs.find_all("img"):
            # print(img.get("src"))
            save_image(path, img.get("src"))
    fpath = os.path.join(path, title + '.txt')
    with open(fpath, 'w') as f:
        if tags:
            f.write("tags:" + tags.encode("utf-8") + "\n")
        if keywords:
            f.write("keywords:" + keywords.encode("utf-8") + "\n")
        if descriptions:
            f.write("descriptions:" + descriptions.encode("utf-8") + "\n")
        f.write("url:" + url + "\n")
        for p_cons in soup.find_all("div", id="artibody"):
            for p_con in p_cons.find_all("p"):
                spans = p_con.find_all("span")
                if spans:
                    content = p_con.find_all("span")[0].string
                    # print p_con.contents[0]
                else:
                    content = p_con.string
                # print(content)
                if content is not None:
                    f.write(content.encode("utf-8") + "\n")
    f.close()


def crawl_home(url):
    resp = requests.get(url, headers=headers)
    page = resp.content
    soup = BeautifulSoup(page, 'lxml', from_encoding='utf-8')
    # print(soup.prettify())
    url_set = set()
    for link in soup.select('a[href*="doc-"]'):
        href = link.get("href")
        # print href
        url_set.add(href)

    # 另外一部分信息需要通过接口获取
    # http://feed.mix.sina.com.cn/api/roll/get?pageid=434&lid=2666&num=10&versionNumber=1.2.4&page=2&encode=utf-8&_=1524216930272
    data = get_data()
    params['page'] = 1
    url_set.update(get_doc_url(data))
    if data:
        # 获取总记录条数
        total = data['result']['total']
        if total <= 0:
            return
        # 计算剩余需要查询的次数
        num = params['num']
        if(total <= num):
            times_left = 0
        else:
            times_left = total // num
            if total % num == 0:
                times_left = times_left - 1
        i = 0
        while i < times_left:
            params['page'] = i + 2
            url_set.update(get_doc_url(get_data()))
            i = i + 1
    i = 1
    lengh = str(len(url_set))
    path = "download"
    isEx = os.path.exists(path)
    if not isEx:
        os.makedirs(path)
    fpath = os.path.join(path, "passed.txt")
    with open(fpath, "w") as f:
        for link_url in url_set:
            print(str(i) + "/" + lengh + ": " + link_url)
            time.sleep(1)
            crawl(link_url)
            f.write(link_url + "\n")
            i = i + 1
            if i % 20 == 0:
                f.flush()
    f.close()

def get_data():
    params['_'] = time.time()
    news_list_url = "http://feed.mix.sina.com.cn/api/roll/get"
    json_con = requests.get(news_list_url, headers=headers_feeds, params=params).content
    data = json.loads(json_con)
    return data

def get_doc_url(data):
    tmp_set = set()
    if data:
        for link_obj in data['result']['data']:
            # print(link_obj['url'])
            tmp_set.add(link_obj['url'])
    return tmp_set

if __name__ == '__main__':
    # url = 'http://finance.sina.com.cn/blockchain/coin/2018-04-19/doc-ifzihnep9257549.shtml'
    url = 'http://finance.sina.com.cn/blockchain/'
    crawl_home(url)