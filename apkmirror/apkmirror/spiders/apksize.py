# -*- coding: utf-8 -*-
import scrapy


class ApksizeSpider(scrapy.Spider):
    name = 'apksize'
    allowed_domains = ['www.apkmirror.com']
    start_urls = [
        'https://www.apkmirror.com/uploads/?q=lite',
    ]

    def parse(self, response):
        for quote in response.xpath('//div[@class="infoSlide"]'):
            datetime = quote.css(
                'p span span[class=datetime_utc]::text'
            ).extract()
            infos = quote.css(
                'p span[class=infoslide-value]::text'
            ).extract()
            yield {
                'version': infos[0],
                'filesize': infos[1],
                'datetime': datetime,
            }
        next_page = response.xpath(
            '//a[@class="nextpostslink"]/@href').extract_first()
        if next_page:
            yield response.follow(next_page, self.parse)
