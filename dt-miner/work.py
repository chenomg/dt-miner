#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
此模块用于调度爬虫模块然后清洗数据并操作数据库
'''
import json

from crawler import AsyncCrawler
from db import MySQL
from table import jobs
from pattern import www_51job


def main():
    index = 'https://search.51job.com/list/020000,000000,0000,00,9,99,python,2,{}.html?lang=c&stype=1&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=4&dibiaoid=0&address=&line=&specialarea=00&from=&welfare='
    index_pages = [index.format(page) for page in range(1, 3)]
    selectors = www_51job.SELECTORS
    index_rule = {key: selectors[key]['xpath_selector'] for key in selectors}
    crawler = AsyncCrawler(
        index_rule=index_rule,
        index_pages=index_pages,
        # headers=rand_header(),
        # cookies=get_cookies(),
        # ajax_data=AJAX_POST_DATA,
        async_wait=20,
        concur_req=5)
    res = crawler.work()
    with open('results.txt', 'w', encoding='utf-8') as f:
        for item in res:
            f.write(json.dumps(item, ensure_ascii=False))
            f.write('\n')


if __name__ == "__main__":
    main()
