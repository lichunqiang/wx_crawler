import scrapy

from demo.items import DemoItem

class DmozSpider(scrapy.Spider):
	"""docstring for DmozSpider"""
	name = 'dmoz'
	allowed_domains  = ['dmoz.org']
	start_urls = (
		"http://www.dmoz.org/Computers/Programming/Languages/Python/Books/",
		"http://www.dmoz.org/Computers/Programming/Languages/Python/Resources/"
	)
	# response is scrapy.http.Response
	def parse(self, response):
		for el in response.xpath('//ul/li'):
			i = DemoItem()
			i['title'] = el.xpath('a/text()').extract()
			i['link'] = el.xpath('a/@href').extract()
			i['desc'] = el.xpath('text()').extract()
			yield i

