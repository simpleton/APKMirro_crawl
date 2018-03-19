#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import scrapy
import copy
import re
from urllib.parse import urljoin
from apkmirror.items import ApkmirrorItem


class ApksizeSpider(scrapy.Spider):
    name = 'apksize'
    allowed_domains = ['www.apkmirror.com']
    url_host = "https://" + allowed_domains[0]
    path_prefix = "uploads/?q="
    size_pattern = re.compile(".*MB")

    def __init__(self, apps_list_file=None, app_name=None, *args, **kwargs):
        super(ApksizeSpider, self).__init__(*args, **kwargs)
        self.url_prefix = urljoin(self.url_host, self.path_prefix)
        if apps_list_file:
            self.start_urls = []
            with open(apps_list_file, 'r') as f:
                for line in f.readlines():
                    self.start_urls.append(self.url_prefix + line.strip())
        else:
            self.start_urls = [f"{self.url_prefix}{app_name}"]
        print(f"Start Url: {self.start_urls}")

    def parse(self, response):
        for quote_title, quote_info in zip(
                response.css("div[id=primary] h5 a[class=fontBlack]"),
                response.xpath('//div[@class="infoSlide"]')):
            fullname = quote_title.xpath("text()").extract_first()
            datetime = quote_info.css(
                'p span span[class=datetime_utc]::text').extract_first()
            infos = quote_info.css(
                'p span[class=infoslide-value]::text'
            ).extract()
            item = ApkmirrorItem(
                app=response.request.url.split("=")[1],
                app_fullname=fullname,
                version=infos[0],
                filesize=infos[1],
                datetime=datetime,
            )
            detail_link = quote_title.xpath("@href").extract_first()
            yield scrapy.Request(
                urljoin(self.url_host, detail_link),
                self.parse_variant,
                meta={'item': item},
            )
        next_page = response.xpath(
            '//a[@class="nextpostslink"]/@href'
        ).extract_first()
        if next_page:
            yield response.follow(next_page, self.parse)

    def parse_variant(self, response):
        item = copy.deepcopy(response.meta['item'])
        for quote in response.xpath('//div[@class="table-row headerFont"]'):
            infos = quote.xpath(
                './/div[@class="table-cell rowheight addseparator expand pad dowrap"]/text()'
            ).extract()
            infos = list(filter(None, [i.strip() for i in infos]))
            if infos:
                variant, datetime, link = self._parse_variant(quote)
                item.update({
                    'arch': infos[0],
                    'min_version': infos[1],
                    'screen_dpi': infos[2],
                    'datetime': datetime,
                    'variant': variant,
                })
                yield scrapy.Request(
                    urljoin(self.url_host, link),
                    self.parse_detail,
                    meta={'item': item},
                )

    def parse_detail(self, response):
        selectors = response.xpath(
            '//div[@class="appspec-row"]/div[@class="appspec-value"]/text()'
        ).extract()
        for sel in selectors:
            match = self.size_pattern.match(sel)
            if match:
                response.meta['item']['filesize'] = match.group()
                yield response.meta['item']

    def _parse_variant(self, response):
        variant = next(v.strip()
                       for v in response.xpath('.//div/a/text()').extract()
                       if v.strip())
        link = response.xpath('.//div/a/@href').extract_first()
        datetime = response.xpath(
            './/span[@class="dateyear_utc"]/@data-utcdate'
        ).extract_first()
        return variant, datetime, link
