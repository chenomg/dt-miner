#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# jobs的表格设计
NAME = 'jobs'

TABLE_CONTENT = {
    # primary key
    'ID': 'INT NOT NULL AUTO_INCREMENT PRIMARY KEY',
    # 工作所在城市
    'City': 'CHAR(100) NOT NULL',
    # 公司名字
    'CompanyName': 'CHAR(100) NOT NULL',
    # 职位名字
    'PositionName': 'CHAR(200) NOT NULL',
    # 工资
    'Salary': 'CHAR(50) NOT NULL',
    # 公司ID
    'CompanyId': 'INT',
    # 公司描述
    'CompanyDescription': 'TEXT',
    # 公司标签
    'CompanyLable': 'CHAR(200)',
    # 公司所在地址
    'CompanyLocation': 'CHAR(200)',
    # 公司规模
    'CompanySize': 'CHAR(50)',
    # 教育程度需求
    'Education': 'CHAR(50)',
    # 融资状态
    'FinanceStage': 'CHAR(50)',
    # 工作分类：一类
    'FirstType': 'CHAR(200)',
    # 所属行业
    'IndustryField': 'CHAR(50)',
    # 职位描述
    'JobDescription': 'TEXT',
    # 职位详情页
    'JobDetailUrl': 'TEXT',
    # 职位编号
    'JobId': 'INT',
    # 工作性质：全职，兼职等
    'JobNature': 'CHAR(10)',
    # 职位优势
    'PositionAdvantage': 'CHAR(200)',
    # 信息发布时间
    'PublishTime': 'CHAR(50)',
    # 招聘人数
    'Recruits': 'INT',
    # 工作分类：二
    'SecondType': 'CHAR(200)',
    # 数据来源，例：'51job.com'
    'SourceFrom': 'CHAR(50)',
    # 工作分类：三
    'ThirdType': 'CHAR(200)',
    # 工作所在地址
    'WorkLocation': 'CHAR(200)',
    # 工作年限要求
    'WorkYear': 'CHAR(20)',
}
