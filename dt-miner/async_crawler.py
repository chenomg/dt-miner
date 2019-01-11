#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import random
import asyncio
import time
import socket

import aiohttp
import requests
from lxml import etree

from db_connector import MySQL_Connector

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

# 从response提取下一页以及详情页的xpath规则
next_page_rule = ''
detail_page_rule = ''

cookie = dict(cookies_are="Your cookie here")


class AsyncCrawler():
    def __init__(self,
                 index_url=None,
                 cookies=None,
                 headers=None,
                 next_page_rule=None,
                 detail_page_rule=None,
                 max_tasks=0):
        self._index_url = index_url
        self._cookies = cookies
        self._headers = headers
        self._next_page_rule = next_page_rule
        self._detail_page_rule = detail_page_rule
        self._max_tasks = int(max_tasks) if int(max_tasks) > 0 else 0

    @peoperty
    def index_url(self):
        return self._index_url

    @index_url.setter
    def index_url(self, index_url):
        self._index_url = index_url

    @index_url.deleter
    def index_url(self):
        del self._index_url

    @peoperty
    def headers(self):
        return self._headers

    @headers.setter
    def headers(self, headers):
        self._headers = headers

    @headers.deleter
    def headers(self):
        del self._headers

    @peoperty
    def cookies(self):
        return self._cookies

    @cookies.setter
    def cookies(self, cookies):
        self._cookies = cookies

    @cookies.deleter
    def cookies(self):
        del self._cookies

    def work(self):
        """
        协程loop, 从详情页response获取相关信息并且调取_db_save进行数据保存
        """
        pass

    def _collect_tasks(self, max_tasks=0):
        """
        输入搜索词后获取详情页网址列表
        """
        pass

    async def _async_fetch(self, url, headers=None, cookies=None):
        """
        异步获取相应网址的response
        """
        async with aiohttp.ClientSession(
                connector=aiohttp.TCPConnector(verify_ssl=False, ),
                headers=headers,
                cookies=cookies,
        ) as session:
            content = await session.get(url)
            return await content

    def _db_save(self):
        """
        将处理后的信息保存到数据库
        """
        pass


def rand_header():
    return {'user-agent': random.choice(HEADERS)}


async def crawler_async(url, index):
    async with aiohttp.ClientSession(
            connector=aiohttp.TCPConnector(verify_ssl=False, ),
            headers=rand_header(),
    ) as session:
        content = await session.get(url)
        return await content
        # with open('page/{}_content.txt'.format(index), 'w') as f:
        # f.write(await content.text())


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
