# coding=utf-8
import os
import requests
import json
import time

headers = {
    "accept": "api.jinse.com",
    # "accept-encoding": "gzip, deflate, br",
    "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
    "origin": "https://www.jinse.com",
    "referer": "https://www.jinse.com/lives",
    'Connection': 'close',
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36",
    "cookie": 'userId=eyJpdiI6Ik9CWmNBVzNmQ1wvbUpjTnNnU1ZCMU13PT0iLCJ2YWx1ZSI6Ik9uS3FPckRLSkJ6RGJaalwvdFQ4MGlkZzZhN3VZa3VSa3JiQmNMWjVyc05ybGViT1VPK093WXpDUmdaVVZaVW50TWxiYUZ0UWY2NlZCRWlNSlRJSXdFdz09IiwibWFjIjoiNWY2YjI4YTZhOTQ1MzY5MWVmNDNmNTAzYmFjN2M0NWMzODQ3NzI4NzdkYTU1NjE2ZDgzZDY4M2Q3M2UyMGUzZCJ9; is_refresh=eyJpdiI6Imx6a3hNaWxna3kyaWVxR0ZDbHV5TUE9PSIsInZhbHVlIjoiVVhpdGQ2anc4ampBTDlMTUdZaHR3UT09IiwibWFjIjoiMTZhNjcxYmM2NjViNmY4YWJhZTNlOWIwZWQ4MDhmMjdmN2E1NDMyMjg1NTIyZDc3OGYzODhiZTcwYTJhMmEyMCJ9; _ga=GA1.2.1878962000.1524537538; _gid=GA1.2.1748138735.1524537538; Hm_lvt_3b668291b682e6dc69686a3e2445e11d=1524537539; Hm_lpvt_3b668291b682e6dc69686a3e2445e11d=1524537823'
}
params = {
    "limit": 20,
}

lasttop = 24732
lastbottom = 172

def save_file(list):
    if not list:
        return

    path = "jinsecaijing"
    for date_info in list:
        date = date_info['date']
        if not path:
            continue
        isEx = os.path.exists(path)
        if not isEx:
            os.makedirs(path)
        fpath = os.path.join(path, str(date) + ".txt")
        with open(fpath, 'a') as f:
            for detail in date_info['lives']:
                id = detail['id']
                if id >= lastbottom and id <= lasttop:
                    continue

                print("id: " + str(detail['id']) + "\n")
                print("content: " + detail['content'].encode("utf-8") + "\n")
                print("create_time: " + str(detail['created_at']) + "\n")

                f.write("id: " + str(detail['id']) + "\n")
                f.write("content: " + detail['content'].encode("utf-8") + "\n")
                f.write("create_time: " + str(detail['created_at']) + "\n")

        f.close()
        print("完成一次保存！" + fpath)


def crawl_all(url, lastbottom):
    if lastbottom > 0:
        params['flag'] = 'down'
        params['id'] = lastbottom

    s = requests.session()
    resp = s.get(url, params=params, headers=headers).content
    s.close()
    if resp == 'Too Many Attempts.':
        time.sleep(60)
        crawl_all(url)
    data = json.loads(resp)
    if data:
        count = data['count']
        botrom_id = data["bottom_id"]
        list = data["list"]

        if count <= 0:
            print("no news")
            return

        save_file(list)

        lastbottom = botrom_id

        while lastbottom > 0:
            params['flag'] = 'down'
            params['id'] = lastbottom
            s = requests.session()
            resp = s.get(url, params=params, headers=headers).content
            s.close()
            if resp == 'Too Many Attempts.':
                time.sleep(60)
                continue
            data = json.loads(resp)
            if data:
                count = data['count']
                botrom_id = data["bottom_id"]
                list = data["list"]

                if count <= 0:
                    print("no news")
                    break
                save_file(list)
                lastbottom = botrom_id
                time.sleep(3)

def crawl_latest(url, lastbottom, lasttop):
    # if lastbottom > 0:
    #     params['flag'] = 'down'
    #     params['id'] = lastbottom

    s = requests.session()
    resp = s.get(url, params=params, headers=headers).content
    s.close()
    if resp == 'Too Many Attempts.':
        time.sleep(60)
        crawl_latest(url)
    data = json.loads(resp)
    if data:
        count = data['count']
        bottom_id = data["bottom_id"]
        top_id = data['top_id']
        list = data["list"]

        if count <= 0:
            print("no news")
            return

        if not ((bottom_id in range(lastbottom, lasttop + 1) and top_id > lasttop) or (bottom_id >= lasttop)):
            print("no news found, exit..\n")
            return

        print("found latest news....downloading..\n")

        save_file(list)

        # 保存latesttopid到文件中
        fpath = os.path.join('jinsecaijing', 'latest.txt')
        with open(fpath, 'w') as f:
            f.write(str(lastbottom) + "|" + str(top_id))
        f.close()

        # 没有最新页，不需要继续爬取，退出
        if bottom_id <= lasttop:
            print("downloading end, exit..\n")

        tmp_bottom = bottom_id
        while bottom_id > lasttop:
            params['flag'] = 'down'
            params['id'] = tmp_bottom
            s = requests.session()
            resp = s.get(url, params=params, headers=headers).content
            s.close()
            if resp == 'Too Many Attempts.':
                time.sleep(60)
                continue
            data = json.loads(resp)
            if data:
                count = data['count']
                bottom_id = data["bottom_id"]
                list = data["list"]

                if count <= 0:
                    print("no news")
                    break
                save_file(list)
                tmp_bottom = bottom_id
                time.sleep(3)

def start_crawl():
    url = "https://api.jinse.com/v4/live/list"
    # 默认值
    lasttop = 24732
    lastbottom = 172
    # 读取lasttop,bottom信息
    # 保存latesttopid到文件中
    fpath = os.path.join('jinsecaijing', 'latest.txt')
    if os.path.exists(fpath):
        with open(fpath, 'r') as f:
            last_info = f.readline()
        if last_info:
            arr = last_info.split("|")
            if arr and len(arr) > 0:
                lastbottom = int(arr[0])
                lasttop = int(arr[1])

    crawl_latest(url, lastbottom, lasttop)

if __name__ == '__main__':
    i = 1
    while i > 0:
        print("start crawling...." + str(i) + "\n")
        start_crawl()
        print("end crawling...." + str(i) + "\n")
        i = i + 1
        time.sleep(30)
