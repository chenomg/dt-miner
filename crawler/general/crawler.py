#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import random
import time

import requests
from lxml import etree

HEADERS = [
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv2.0.1) Gecko/20100101 Firefox/4.0.1",
    "Mozilla/5.0 (Windows NT 6.1; rv2.0.1) Gecko/20100101 Firefox/4.0.1",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11",
    "Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/602.2.14 (KHTML, like Gecko) Version/10.0.1 Safari/602.2.14',
    'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'
]

cookie = dict(cookies_are="Your cookie here")


class BaseCrawler():
    def __init__(self, url=None, config=None):
        self._url = url
        self._config = config

    def rand_header(self):
        return {'user-agent': random.choice(HEADERS)}

    def get_data(self):
        rst = requests.get(
            self._url, headers=self.rand_header(), cookies=cookie)
        return rst.content.decode('utf-8')


def sub_urls(url, rule=None):
    c = BaseCrawler(url=url)
    page = c.get_data()
    html = etree.HTML(page)
    url_list = [url for url in html.xpath('//div[@class="title"]/a/@href')]
    return url_list


def main():
    url = 'https://sh.lianjia.com/ershoufang/'
    urls = sub_urls(url)
    t_s = time.time()
    index = 0
    for url in urls:
        p = BaseCrawler(url=url)
        data = p.get_data()
        with open('page/{}_content.txt'.format(index), 'w') as f:
            f.write(data)
        index += 1
        time.sleep(0.1)
    t_e = time.time()
    print('time cost: {:.3f}s'.format(t_e - t_s))


if __name__ == "__main__":
    main()
