#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ApkmirrorItem(scrapy.Item):
    # define the fields for your item here like:
    app = scrapy.Field()
    app_fullname = scrapy.Field()
    version = scrapy.Field()
    datetime = scrapy.Field()
    filesize = scrapy.Field()
    variant = scrapy.Field()
    arch = scrapy.Field()
    min_version = scrapy.Field()
    screen_dpi = scrapy.Field()
