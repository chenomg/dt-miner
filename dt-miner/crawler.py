#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import random
import asyncio
import time
import socket
import collections
import copy
import json

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

DATA_RULE = {
    'job_title': '//div[@class="position"]/div/a/h3/text()',
    'salary': '//span[@class="salary"]/text()',
}

AJAX_POST_DATA = {
    'url':
    'https://www.lagou.com/jobs/positionAjax.json?city=%E4%B8%8A%E6%B5%B7&needAddtionalResult=false',
    'method':
    'post',
    'form': {
        'first': 'false',
        'pn': '2',
        'kd': 'python',
    },
}

CONCUR_REQ = 1


class AsyncCrawler():
    # 返回相应的数据，dict type
    def __init__(self,
                 index_url=None,
                 index_pages=None,
                 cookies=None,
                 headers=None,
                 index_rule=None,
                 data_rule=None,
                 ajax_data=None,
                 concur_req=0):
        self._index_url = index_url
        self._index_pages = index_pages if not index_url else None
        self._cookies = cookies
        self._headers = headers
        self._index_rule = index_rule
        self._data_rule = data_rule
        self._ajax_data = ajax_data
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

    @property
    def ajax_data(self):
        return self._ajax_data

    @ajax_data.setter
    def ajax_data(self, value):
        self._ajax_data = value

    @ajax_data.deleter
    def ajax_data(self):
        del self._ajax_data

    def get_data_ajax(self):
        """
        通过ajax获取多页数据
        """
        if not self._ajax_data:
            raise ValueError
        num = 3
        urls = self._ajax_data['url']
        post_data = self._ajax_data
        post_json_data = [
            copy.deepcopy(post_data)
            for post_data['form']['pn'] in range(1, num + 1)
        ]
        method = self._ajax_data['method']
        print('ajax_method&', method, post_json_data, urls)
        results = self._coro_loop(
            urls_to_work=urls,
            concur_req=self._concur_req,
            method=method,
            post_json_data=post_json_data)
        return results

    def get_data(self):
        """
        输入搜索词后获取详情页网址列表
        """
        data = []
        detail_pages = self._collect_tasks(self, index_pages=self._index_pages)
        results = self._coro_loop(self, self._concur_req, self._data_rule)
        for page in results:
            for url in page['url']:
                detail_pages.append(url)
        if max_tasks and len(detail_pages) >= max_tasks:
            detail_pages = detail_pages[:max_tasks]
        with open('detail_pages.txt', 'w', encoding='utf-8') as f:
            for item in detail_pages:
                f.write(item)
                f.write('\n')
        return detail_pages

    def _collect_tasks(self, index_url=None, index_pages=None, max_tasks=0):
        """
        输入搜索词后获取详情页网址列表
        """
        detail_pages = []
        results = self._coro_loop(index_pages, self._concur_req,
                                  self._index_rule)
        for page in results:
            for url in page['url']:
                detail_pages.append(url)
        if max_tasks and len(detail_pages) >= max_tasks:
            detail_pages = detail_pages[:max_tasks]
        try:
            with open('detail_pages.txt', 'w', encoding='utf-8') as f:
                for item in detail_pages:
                    f.write(item)
                    f.write('\n')
        except Exception as e:
            print(e)
        return detail_pages

    def _coro_loop(self,
                   urls_to_work,
                   concur_req,
                   data_rule=None,
                   method='get',
                   post_json_data=None):
        """
        协程loop, 从response获取相关信息
        """
        if not concur_req:
            concur_req = len(urls_to_work)
        print('concur_req:', concur_req, urls_to_work)
        self._semaphore = asyncio.Semaphore(concur_req)
        loop = asyncio.get_event_loop()
        coro = self._fetch_coro(
            urls_to_work,
            concur_req,
            data_rule,
            method=method,
            post_json_data=post_json_data)
        results = loop.run_until_complete(coro)
        loop.close()
        return results

    async def _fetch_coro(self, urls_to_work, concur_req, data_rule, method,
                          post_json_data):
        """
        异步从多个网址的response中提取数据,data_rule为None时返回包含所有response列表
        """
        # 用于存放返回的数据
        result = []
        counter = collections.Counter()
        if method == 'get':
            to_do = [
                self._fetch_one(url, method, post_json_data)
                for url in urls_to_work
            ]
        if method == 'post':
            urls = [url['url'] for url in post_json_data]
            post_json_datas = [data['form'] for data in post_json_data]
            to_do = [
                self._fetch_one(url, method, post_data)
                for url, post_data in zip(urls, post_json_datas)
            ]
        to_do_iter = asyncio.as_completed(to_do)
        for future in to_do_iter:
            try:
                print('try getting future...')
                response = await future
                print('got future response...')
                if data_rule:
                    print('got it!')
                    html = etree.HTML(response)
                    res_dict = {}
                    for key, rule in data_rule.items():
                        res_dict[key] = [
                            data.strip() for data in html.xpath(rule)
                        ]
                    result.append(res_dict)
                else:
                    result.append(response)
            except Exception as e:
                print('fetch_coro_Error:', e)
        return result

    async def _fetch_one(self, session, url, method, post_json_data):
        """
        异步获取相应网址的response
        """
        print('url:', url, '\nmethod:', method, '\npost_json_data:',
              post_json_data)
        with (await self._semaphore):
            async with aiohttp.ClientSession(
                    connector=aiohttp.TCPConnector(verify_ssl=False, ),
                    headers=self._headers,
                    cookies=self._cookies,
            ) as session:
                print('waitting for results')
                if method == 'get':
                    content = await session.get(url)
                if method == 'post':
                    if not post_json_data:
                        post_json_data = self._post_json_data
                    content = await session.post(url, data=post_json_data)
                    print('got content')
                return await content.text()

    def _db_save(self):
        """
        将处理后的信息保存到数据库
        """
        pass


def rand_header():
    return {
        'Accept':
        'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding':
        'gzip, deflate, br',
        'Accept-Language':
        'en,zh-CN;q=0.9,zh;q=0.8',
        'Connection':
        'keep-alive',
        'Content-Length':
        '29',
        'Content-Type':
        'application/x-www-form-urlencoded; charset=UTF-8',
        'User-Agent':
        random.choice(HEADERS),
        'DNT':
        '1',
        'Host':
        'www.lagou.com',
        'Origin':
        'https://www.lagou.com',
        'Referer':
        'https://www.lagou.com/jobs/list_pyhton%20web?labelWords=&fromSearch=true&suginput=',
        'X-Anit-Forge-Code':
        '0',
        'X-Anit-Forge-Token':
        'None',
        'X-Requested-With':
        'XMLHttpRequest',
    }


def get_cookies():
    cookies = {}
    with open('cookies.key') as c:
        for item in c.read().split(';'):
            name, value = item.strip().split('=', 1)
            cookies[name] = value
    return cookies


def main():
    lagou_index = 'https://www.lagou.com/zhaopin/Python/{}/'
    index_pages = [lagou_index.format(page) for page in range(1, 31)]
    crawler = AsyncCrawler(
        headers=rand_header(),
        cookies=get_cookies(),
        ajax_data=AJAX_POST_DATA,
        concur_req=5)
    res = crawler.get_data_ajax()
    with open('ajax_data.txt', 'w', encoding='utf-8') as f:
        for item in res:
            f.write(json.dumps(item, ensure_ascii=False))
            f.write('\n')
    print(res)


if __name__ == "__main__":
    main()
