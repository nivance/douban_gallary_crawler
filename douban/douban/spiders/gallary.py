# -*- coding: utf-8 -*-

import os
import random

import requests
import scrapy

ablum_url = 'https://www.douban.com/photos/album/{}/?m_start='


def random_user_agent():
    return random.choice(user_agent_list)


class GallarySpider(scrapy.Spider):
    name = "gallary"

    def __init__(self):
        # 相册下载目录
        self.gallary_download_dir = ''
        # 相册id
        self.album_id = ''

    def start_requests(self):
        self.gallary_download_dir = self.settings.attributes['GALLARY_DOWNLOAD_DIR'].value
        self.album_id = self.settings.attributes['ALBUM_ID'].value
        base_url = ablum_url.format(self.album_id)
        page_size = self.settings.attributes['PAGE_SIZE'].value
        page_items = 18
        urls = []
        for i in range(page_size):
            urls.append(base_url + str(i * page_items))
        print(urls)
        headers = {'User-Agent': random_user_agent()}
        for url in urls:
            yield scrapy.Request(url=url, headers=headers, callback=self.parse)

    def parse(self, response):
        # 相册名称
        gallary_name = response.xpath('//*[@id="db-usr-profile"]/div[2]/h1')[0].root.text.replace('\n', '').replace(' ',
                                                                                                                    '')
        # 图片保存路劲
        gallary_dir = self.gallary_download_dir + gallary_name
        if not os.path.exists(gallary_dir):
            os.makedirs(gallary_dir)
        elements = response.xpath('/html/body/div[3]/div[1]/div[2]/div[1]/div[2]/div')
        for element in elements:
            # print(element)
            if element.root.attrib['class'] == 'photo_wrap':
                img_url = element.xpath('.//a//img').attrib['src']
                image_path = gallary_dir + img_url.split('/')[-1]
                # 使用Scrapy的FilePipeline来处理文件下载
                # yield {
                #     'url': img_url,
                #     'path': image_path,
                #     'headers': {'User-Agent': random_user_agent()}
                # }
                print(img_url)
                self.download_image(img_url, gallary_dir)

    def download_image(self, image_url, gallary_dir):
        response = requests.get(image_url, headers={'User-Agent': random_user_agent()}, stream=True)
        # 确保请求成功
        if response.status_code == 200:
            image_path = os.path.join(gallary_dir, image_url.split('/')[-1])
            if not os.path.isfile(image_path):
                # 打开一个本地文件用于保存图片，你可以根据需要修改文件名和路径
                with open(image_path, 'wb') as file:
                    # 将获取到的图片数据写入文件
                    for chunk in response.iter_content(1024):
                        file.write(chunk)
                print("图片下载成功，保存为" + image_path)
        else:
            print("图片下载失败，错误代码：", response.status_code)


# the default user_agent_list composes chrome,I E,firefox,Mozilla,opera,netscape
# for more user agent strings,you can find it in http://www.useragentstring.com/pages/useragentstring.php
user_agent_list = [
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 "
    "(KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
    "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 "
    "(KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 "
    "(KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 "
    "(KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 "
    "(KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 "
    "(KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 "
    "(KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 "
    "(KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 "
    "(KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 "
    "(KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 "
    "(KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 "
    "(KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 "
    "(KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 "
    "(KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 "
    "(KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 "
    "(KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 "
    "(KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 "
    "(KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
]
