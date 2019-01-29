#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# jobs的表格设计
NAME = 'jobs'

TABLE_CONTENT = {
    # primary key
    'ID': 'INT NOT NULL AUTO_INCREMENT PRIMARY KEY',
    # 工作所在城市
    'City': 'VARCHAR(100) NOT NULL',
    # 公司名字
    'CompanyName': 'VARCHAR(100) NOT NULL',
    # 职位名字
    'PositionName': 'VARCHAR(200) NOT NULL',
    # 工资
    'Salary': 'float NOT NULL',
    # 公司ID
    'CompanyId': 'INT',
    # 公司描述
    'CompanyDescription': 'TEXT',
    # 公司标签
    'CompanyLable': 'VARCHAR(200)',
    # 公司所在地址
    'CompanyLocation': 'VARCHAR(200)',
    # 公司规模
    'CompanySize': 'VARCHAR(50)',
    # 教育程度需求
    'Education': 'VARCHAR(50)',
    # 融资状态
    'FinanceStage': 'VARCHAR(50)',
    # 工作分类：一类
    'FirstType': 'VARCHAR(200)',
    # 所属行业
    'IndustryField': 'VARCHAR(50)',
    # 职位描述
    'JobDescription': 'TEXT',
    # 职位编号
    'JobId': 'INT',
    # 工作性质：全职，兼职等
    'JobNature': 'VARCHAR(10)',
    # 职位优势
    'PositionAdvantage': 'VARCHAR(200)',
    # 信息发布时间
    'PublishTime': 'VARCHAR(50)',
    # 招聘人数
    'Recruits': 'INT',
    # 工作分类：二
    'SecondType': 'VARCHAR(200)',
    # 工作分类：三
    'ThirdType': 'VARCHAR(200)',
    # 工作所在地址
    'WorkLocation': 'VARCHAR(200)',
    # 工作年限要求
    'WorkYear': 'VARCHAR(20)',
}
