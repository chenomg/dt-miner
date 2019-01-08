#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import random
import asyncio
import time
import socket

import aiohttp
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


def rand_header():
    return {'user-agent': random.choice(HEADERS)}


async def crawler_async(url, index):
    async with aiohttp.ClientSession(
            connector=aiohttp.TCPConnector(verify_ssl=False, ),
            headers=rand_header(),
    ) as session:
        content = await session.get(url)
        with open('page/{}_content.txt'.format(index), 'w') as f:
            f.write(await content.text())


def crawler(url):
    rst = requests.get(url, headers=rand_header(), cookies=cookie)
    return rst.content.decode('utf-8')


def sub_urls(url, rule=None):
    page = crawler(url)
    html = etree.HTML(page)
    # url_list = [url for url in html.xpath('//div[@class="title"]/a/@href')]
    url_list = [url for url in html.xpath('//div[@class="p_top"]/a/@href')]
    return url_list


def main():
    # url = 'https://sh.lianjia.com/ershoufang/'
    url = 'https://www.lagou.com/zhaopin/Python/?labelWords=label'
    urls = sub_urls(url)
    to_do = [crawler_async(urls[i], i) for i in range(len(urls))]
    wait_cor = asyncio.wait(to_do)
    t_s = time.time()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(wait_cor)
    t_e = time.time()
    print('time cost: {:.3f}s'.format(t_e - t_s))


if __name__ == "__main__":
    main()
