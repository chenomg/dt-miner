#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import random
import asyncio
import time

import aiohttp
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

cookie = dict(cookies_are="_ga=GA1.2.1401474153.1523280627; \
    user_trace_token=20180409213027-2a50b8b2-3bfa-11e8-b742-5254005c3644; \
    LGUID=20180409213027-2a50bc8d-3bfa-11e8-b742-5254005c3644; \
    index_location_city=%E4%B8%8A%E6%B5%B7; \
    JSESSIONID=ABAAABAAADEAAFI636092B5659CA18CEB97FBA077E04C12; \
    _gid=GA1.2.2012477522.1546230622; \
    Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1544709432,1546007647,1546230622; \
    TG-TRACK-CODE=index_navigation; \
    LGSID=20181231165843-461a9e8d-0cda-11e9-b48a-525400f775ce; \
    _gat=1; \
    SEARCH_ID=2e7a20283d8e4c9e838f822bcfdff96c; \
    Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1546249139; \
    LGRID=20181231173929-f86f5c1f-0cdf-11e9-ae7e-5254005c3644")


class BaseCrawler():
    def __init__(self, url=None, config=None):
        self._url = url
        self._config = config

    def rand_header(self):
        return {'user-agent': random.choice(HEADERS)}

    async def get_data(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(self._url, headers=self.rand_header(), cookies=cookie) as resp:
                await resp
        # rst = await aiohttp.get(
            # self._url, headers=self.rand_header(), cookies=cookie)
        return rst.content.decode('utf-8')


def sub_urls(url, rule=None):
    c = BaseCrawler(url=url)
    page = c.get_data()
    html = etree.HTML(page)
    url_list = [url for url in html.xpath('//div[@class="p_top"]/a/@href')]
    return url_list


async def _loop(urls, loop):
    index = 0
    tasks = []

    async def process(url):
        p = BaseCrawler(url=url)
        data = await p.get_data()
        with open('page/{}_content.txt'.format(index), 'w') as f:
            f.write(data)
        index += 1
        time.sleep(0.1)

    for url in urls:
        tasks.append(loop.create_task(process(url)))
    await asyncio.wait(tasks)


def main():
    url = 'https://www.lagou.com/zhaopin/Python/?filterOption=3'
    urls = sub_urls(url)
    t_s = time.time()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(_loop(urls, loop))
    loop.close()
    t_e = time.time()
    print('time cost: {:.3f}s'.format(t_e - t_s))


if __name__ == "__main__":
    main()
