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
        async_wait=10,
        concur_req=5)
    res = crawler.work()
    with open('results.txt', 'w', encoding='utf-8') as f:
        for item in res:
            f.write(json.dumps(item, ensure_ascii=False))
            f.write('\n')
    # 连接MySQL并持久化数据
    conf = MySQL.load_config()
    db = MySQL(conf['host'], conf['user'], conf['password'], conf['db'])
    db.drop_table(jobs.NAME)
    db.creat_table_if_not_exist(jobs.NAME, jobs.TABLE_CONTENT)
    for items in res:
        length = 10000
        for item in items:
            print('length of {}: {}'.format(item, len(items[item])))
            if len(items[item]) < length:
                length = len(items[item])
        for i in range(length):
            ins_data = {key: items[key][i] for key in items}
            ins_res = db.insert(jobs.NAME, ins_data)
    # print(ins_res)
    db.close()


if __name__ == "__main__":
    main()
