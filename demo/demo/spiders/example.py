# -*- coding: utf-8 -*-
import scrapy


class ExampleSpider(scrapy.Spider):
    name = "example"
    allowed_domains = ["findingschool.com"]
    start_urls = (
        'http://www.findingschool.com/',
    )

    def __init__(self, category = None, *args, **kwargs):
    	"""
		scrapy crawl example -a category=test
    	"""
    	super(ExampleSpider, self).__init__(*args, **kwargs)
    	self.start_urls = ['http://findingschool.net/%s' % category]

    def parse(self, response):
    	"""
		Can return Item or scrapy.Request to get followed links
    	"""
        pass
