#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json


class ApkmirrorPipeline(object):
    def __init__(self):
        self.file_map = {}

    def close_spider(self, spider):
        for _, file in self.file_map.items():
            file.close()

    def process_item(self, item, spider):
        app_name = item['app']
        if app_name not in self.file_map:
            self.file_map[app_name] = open(f'./out/{app_name}.json', 'w')
        else:
            line = json.dumps(dict(item)) + "\n"
            self.file_map[app_name].write(line)
        return item
