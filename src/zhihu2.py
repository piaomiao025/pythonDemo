from selenium import webdriver
import time
from bs4 import BeautifulSoup
from lxml import html
import os
import requests

headers = {
    'Host': 'www.zhihu.com',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Connection': 'keep-alive',
    # 'Accept-Encoding': 'gzip, deflate, br',
    'Cache-Control': 'no-cache',
    'Upgrade-Insecure-Requests': '1',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
}

def save(text, filename='temp', path='download'):
    fpath = os.path.join(path, filename)
    with open(fpath, 'wb') as f:
        print('output:', fpath)
        f.write(text)

def save_image(image_url):
    resp = requests.get(image_url)
    page = resp.content
    filename = image_url.split('zhimg.com/')[-1]
    save(page, filename)

# def crawl(url):
#     resp = requests.get(url, headers = headers)
#     page = resp.content
#     root = html.fromstring(page)
#     image_urls = root.xpath('//img[@data-original]/@data-original')
#     for image_url in image_urls:
#         save_image(image_url)


def main():
    driver = webdriver.Chrome(executable_path="D:/app/python/chromedriver.exe")
    driver.get("https://www.zhihu.com/question/27364360")

    def execute_times(times):
        for i in range(times):
            driver.execute_script("window.scrollTo(0, 0);")
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)
            # try:
            #     # driver.find_element_by_css_selector('button.QuestionMainAction').click()
            #     print("page" + str(i))
            #     time.sleep(1)
            # except:
            #     break

    execute_times(30)

    result_raw = driver.page_source
    # result_soup = BeautifulSoup(result_raw, 'html.parser')
    root = html.fromstring(result_raw)
    image_urls = root.xpath('//img[@data-original]/@data-original')
    for image_url in image_urls:
        save_image(image_url)


if __name__ == '__main__':
    url = 'https://www.zhihu.com/question/27364360'
    main()