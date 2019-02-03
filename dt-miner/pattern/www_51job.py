#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# 51job网站数据获取规则
WEB_SITE = 'https://www.51job.com/'

TABLE = 'jobs'

# 任务页面结构表
PAGE_STRUCTURE = {
    'PositionDetail': '//div[@class="el"]/p[@class="t1"]/span/a/@href',
    'CompanyDetail': '//div[@class="el"]/span[@class="t2"]/a/@href',
}

# xpath_selectors
SELECTORS = {
    'IndexDataBlock': {
        # 索引页一个职位的信息块，若数据不全则丢弃该条数据
        'xpath': '//div[@class="el"]'
    },
    'City': {
        'page': 'index',
        'needed': True,
        'xpath': 'span[@class="t3"]/text()'
    },
    'CompanyName': {
        'page': 'index',
        'needed': True,
        'xpath': 'span[@class="t2"]/a/text()'
    },
    'PositionName': {
        'page': 'index',
        'needed': True,
        'xpath': 'p/span/a/@title'
    },
    'Salary': {
        'page': 'index',
        'needed': True,
        'xpath': 'span[@class="t4"]/text()'
    },
    'JobId': {
        'page': 'index',
        'needed': False,
        'default': 0,
        'xpath': 'p/input/@value'
    },
    'PublishTime': {
        'page': 'index',
        'needed': True,
        'xpath': 'span[@class="t5"]/text()'
    },
}
