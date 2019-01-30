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
    'City': {
        'page': 'index',
        'xpath_selector': '//div[@class="el"]/span[@class="t3"]/text()'
    },
    'CompanyName': {
        'page': 'index',
        'xpath_selector': '//div[@class="el"]/span[@class="t2"]/a/text()'
    },
    'PositionName': {
        'page': 'index',
        'xpath_selector': '//div[@class="el"]/p/span/a/@title'
    },
    'Salary': {
        'page': 'index',
        # 部分职位没有工资，待优化
        'xpath_selector': '//div[@class="el"]/span[@class="t4"]/text()'
    },
    'JobId': {
        'page': 'index',
        'xpath_selector': '//div[@class="el"]/p/input/@value'
    },
    'PublishTime': {
        'page': 'index',
        'xpath_selector': '//div[@class="el"]/span[@class="t5"]/text()'
    },
}
