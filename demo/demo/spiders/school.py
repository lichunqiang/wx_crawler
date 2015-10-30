# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from demo.items import DemoItem


class SchoolSpider(CrawlSpider):
    name = 'school'
    allowed_domains = ['findingschool.net']
    start_urls = ['http://www.findingschool.net/browse']

    rules = (
        Rule(LinkExtractor(allow=('summerbrowse*', 'item\.html')), callback='parse_item'),
    )

    def parse_item(self, response):
        self.logger.info('hi, page %s' % response.url)
        return scrapy.Request(response.url, callback = self.parse_item)
