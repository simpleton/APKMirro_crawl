#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import scrapy


class ApksizeSpider(scrapy.Spider):
    name = 'apksize'
    allowed_domains = ['www.apkmirror.com']
    url_prefix = "https://www.apkmirror.com/uploads/?q="

    def __init__(self, apps_list_file=None, app_name=None, *args, **kwargs):
        super(ApksizeSpider, self).__init__(*args, **kwargs)
        if apps_list_file:
            self.start_urls = []
            with open(apps_list_file, 'r') as f:
                for line in f.readlines():
                    self.start_urls.append(self.url_prefix + line.strip())
        else:
            self.start_urls = [f"{self.url_prefix}{app_name}"]
        print(f"Start Url:{self.start_urls}")

    def parse(self, response):
        for quote_title, quote_info in zip(
                response.css("div[id=primary] h5 a[class=fontBlack]::text"),
                response.xpath('//div[@class="infoSlide"]')):
            fullname = quote_title.extract()
            datetime = quote_info.css(
                'p span span[class=datetime_utc]::text').extract()
            infos = quote_info.css(
                'p span[class=infoslide-value]::text'
            ).extract()

            yield {
                'app': response.request.url.split("=")[1],
                'app_fullname': fullname,
                'version': infos[0],
                'filesize': infos[1],
                'datetime': datetime,
            }
        next_page = response.xpath(
            '//a[@class="nextpostslink"]/@href').extract_first()
        if next_page:
            yield response.follow(next_page, self.parse)
