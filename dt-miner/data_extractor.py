#!/usr/bin/env python
# encoding: utf-8

"""
此模块用于从crawler爬取的页面中根据提供的规则提取相关数据
"""

def _get_data_from_response(self, response, data_rule):
    # 用于从response中提取指定数据，如存在IndexDataBlock则校验数据是否都存在
    print('Getting data with Rule!')
    html = etree.HTML(response)
    res_dict = {}
    if data_rule:
        if 'IndexDataBlock' in data_rule:
            # 导航页每条数据集
            for block in html.xpath(data_rule['IndexDataBlock']):
                block_res = {}
                for key, value in data_rule.items():
                    # 此项数据不在index页中
                    if value['page'] != 'index':
                        continue
                    # 此项不是需要提取的数据
                    if key == 'IndexDataBlock':
                        continue
                    # 不存在此项数据
                    if not block.xpath(value['xpath']):
                        # 必选项不存在则放弃
                        if value.get('needed'):
                            block_res = {}
                            break
                        # 使用默认数据
                        else:
                            block_res[key] = value['default']
                            continue
                    # 存在此项数据
                    else:
                        block_res[key] = block.xpath(
                            value['xpath'])[0].strip()
                # 将数据加入返回的字典
                if block_res:
                    for key, value in block_res.items():
                        if not res_dict.get(key):
                            res_dict[key] = []
                        res_dict[key].append(value)
        else:
            for key, value in data_rule.items():
                res_dict[key] = [
                    data.strip() for data in html.xpath(value['xpath'])
                ]
        return res_dict
    else:
        return response

