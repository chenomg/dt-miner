#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import random
import asyncio
import time
import socket
import collections

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
INDEX_RULE = {
    'job_title': '//div[@class="p_top"]/a/h3/text()',
    'url': '//div[@class="p_top"]/a/@href'
}
DATA_RULE = {'desc': '//div[@class="position"]/div/a/h3/text()'}
CONCUR_REQ = 1


class AsyncCrawler():
    # 返回相应的数据，dict type
    def __init__(self,
                 index_url=None,
                 cookies=None,
                 headers=None,
                 index_rule=None,
                 data_rule=None,
                 concur_req=0):
        self._index_url = index_url
        self._cookies = cookies
        self._headers = headers
        self._index_rule = index_rule
        self._data_rule = data_rule
        self._concur_req = int(concur_req) if int(concur_req) > 0 else 0

    @property
    def index_url(self):
        return self._index_url

    @index_url.setter
    def index_url(self, index_url):
        self._index_url = index_url

    @index_url.deleter
    def index_url(self):
        del self._index_url

    @property
    def headers(self):
        return self._headers

    @headers.setter
    def headers(self, headers):
        self._headers = headers

    @headers.deleter
    def headers(self):
        del self._headers

    @property
    def cookies(self):
        return self._cookies

    @cookies.setter
    def cookies(self, cookies):
        self._cookies = cookies

    @cookies.deleter
    def cookies(self):
        del self._cookies

    def _collect_tasks(self, key_word=None, max_tasks=0):
        """
        输入搜索词后获取详情页网址列表
        """
        tasks = []
        lagou_index = 'https://www.lagou.com/zhaopin/Python/{}/'
        index_pages = [lagou_index.format(page) for page in range(1, 5)]
        results = self._coro_loop(index_pages, self._concur_req,
                                  self._index_rule)
        for page in results:
            for url in page['url']:
                tasks.append(url)
        if max_tasks and len(tasks) >= max_tasks:
            tasks = tasks[:max_tasks]
        with open('results.txt', 'w', encoding='utf-8') as f:
            for item in tasks:
                f.write(item)
                f.write('\n')
        return tasks

    def _coro_loop(self, urls_to_work, concur_req, data_rule):
        """
        协程loop, 从response获取相关信息
        """
        if not concur_req:
            concur_req = len(urls_to_work)
            self._semaphore = asyncio.Semaphore(concur_req)
            print('concur_req:', concur_req, urls_to_work)
        loop = asyncio.get_event_loop()
        coro = self._fetch_coro(urls_to_work, concur_req, data_rule)
        results = loop.run_until_complete(coro)
        print(results)
        loop.close()
        return results

    async def _fetch_coro(self, urls_to_work, concur_req, data_rule):
        """
        异步从多个网址的response中提取数据
        """
        # 用于存放返回的数据
        result = []
        counter = collections.Counter()
        to_do = [self._fetch_one(url) for url in urls_to_work]
        to_do_iter = asyncio.as_completed(to_do)
        for future in to_do_iter:
            try:
                response = await future
                print('got it!')
                html = etree.HTML(response)
                res_dict = {}
                for key, rule in data_rule.items():
                    res_dict[key] = [data.strip() for data in html.xpath(rule)]
                result.append(res_dict)
            except Exception as e:
                print(e)
        return result

    async def _fetch_one(self, url):
        """
        异步获取相应网址的response
        """
        with (await self._semaphore):
            async with aiohttp.ClientSession(
                    connector=aiohttp.TCPConnector(verify_ssl=False, ),
                    headers=self._headers,
                    cookies=self._cookies,
            ) as session:
                print('waitting for results')
                content = await session.get(url)
                return await content.text()

    def _db_save(self):
        """
        将处理后的信息保存到数据库
        """
        pass


def rand_header():
    return {'user-agent': random.choice(HEADERS)}


def get_cookies():
    cookies = {}
    with open('cookies.key') as c:
        for item in c.read().split(';'):
            name, value = item.strip().split('=', 1)
            cookies[name] = value
    return cookies


def main():
    crawler = AsyncCrawler(
        index_rule=INDEX_RULE, headers=rand_header(), cookies=get_cookies())
    res = crawler._collect_tasks()
    print(res)


if __name__ == "__main__":
    main()
