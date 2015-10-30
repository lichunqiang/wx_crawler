# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Field, Item

class DemoItem(Item):
	"""
	The dmoz example item
	@see http://doc.scrapy.org/en/1.0/intro/tutorial.html#intro-tutorial
	"""
	title = Field()
	link = Field()
	desc = Field()


class DoubanbookItem(Item):
    # define the fields for your item here like:
    # name = Field()
    title = Field()
    link = Field()
    desc = Field()
    num = Field()


class DoubanSubjectItem(Item):
    title = Field()
    link = Field()
    info = Field()
    rate = Field()
    votes = Field()
    content_intro = Field()
    author_intro = Field()
    tags = Field()
