# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from weixin.items import ArticleweixinItem as OutputItem
from weixin.settings import QUERYFILE

from afieldxpath import itemxpath, field_xpath

import re
import urllib
import urlparse


class SogouSpider(CrawlSpider):

    subn = re.compile("<em>|<!--red_beg-->|<!--red_end-->|</em>|<h3>|</h3>")
    name = "sogou"
    allowed_domains = ["sogou.com"]
    start_urls = ["http://weixin.sogou.com/weixin?type=2&query=美国留学&ie=utf8"]
    rules = [
    	Rule(LinkExtractor(allow = ('/websearch/art\.jsp*')), callback = 'parse_items', follow = True)
        #?num=100&query=%E7%BE%8E%E5%9B%BD&tsn=0&type=2&page=2&ie=utf8
        # Rule(LinkExtractor(allow=(r'\?num=\d+&query=.*&tsn=\d&type=\d&page=\d+.*')), callback = "parse_items", follow=True),
        # Rule(LinkExtractor(allow=(r'http://weixin.sogou.com/weixin\?num=\d+&type=\d&query=.*&tsn=\d.*')), callback="parse_items", follow=True),
        # Rule(LinkExtractor(allow=(r'/gzh\?openid=[_a-zA-Z0-9]+',)),callback = "parse_items", follow = True)
    ]

    # 用于
    def get_all(self, response):
    	self.logger.info('Geti................')
        sel = Selector(response)
        items = sel.xpath(itemxpath)
        return items

    def get_nickname(self, node):
        if node:
            st = node.extract()
            startpos = st.find('write(cutLength(\'')
            endpos = st.rfind('\', 16))')

            if (endpos > startpos) and (startpos > 0):
                t = st[startpos + 17:endpos]
                return t

        return None

    # 分析文章链接中的参数
    def _get_param(self, node, param):
        if not node:
            return None

        uri = self.get_articleuri(node)

        if uri:
            value = urlparse.parse_qs(urlparse.urlsplit(uri).query)[param][0]
            return value

        return None

    def get_serid(self, node):
        return self._get_param(node, "__biz")

    def get_mid(self, node):
        return self._get_param(node, "mid")

    def get_idx(self, node):
        return self._get_param(node, "idx")

    def get_sn(self, node):
        return self._get_param(node, "sn")

    def get_title(self, node):
        if node:
            html_part = node.extract()
            if not html_part:
                return None

            article, count = self.subn.subn("", html_part)
            return article

        return None

    def get_summary(self, node):
        if node:
            html_part = node.extract()
            if not html_part:
                return None

            summary, count = self.subn.subn("", html_part)

            return summary

        return None

    def get_cover(self, node):
        if not node:
            return None

        uri = node.extract()

        if len(uri) > 0:
            return uri[0]

        return None

    def get_updatetime(self, node):
        if node:
            st = node.extract()
            startpos = st.find('write(\'')
            endpos = st.rfind('\')')
            t = st[startpos + 7:endpos]

            if t.isdigit():
                return t

        return None

    def get_articleuri(self, node):
        if not node:
            return None

        uri = node.extract()
        return uri

    def get_sogougzh(self, node):
        if not node:
            return None

        uri = node.extract()
        return uri


    # 每个字段对应的处理函数.
    field_action = {
        "sogougzh": get_sogougzh,
        "cover": get_cover,
        "nickname": get_nickname,
        "title": get_title,
        "serid": get_serid,
        "articleuri": get_articleuri,
        "summary": get_summary,
        "mid": get_mid,
        "idx": get_idx,
        "sn": get_sn,
        "updatetime": get_updatetime}


    def parse_type(self, node):
        return

    def parse_items(self, response):
        items = self.get_all(response)

        res = []
        self.logger.info("There are %s items in page %s." % (len(items), response.url))
        for item in items:
            info = OutputItem()
            for field in field_xpath.keys():
                node = item.xpath(field_xpath[field])
                if not node:
                    pass
                else:
                    self.logger.debug("For field %s, get a node." % field)
                    node = node[0]
                    self.logger.debug("Perform field_action get_%s, ." % field)
                    value = self.field_action.get(field)(self, node)
                    self.logger.debug(field + ":" + repr(value))
                    info[field] = value
            self.logger.info("Add a new item.")
            res.append(info)

        self.logger.info("Scrapy %s items from the page %s." % (len(res), response.url))
        return res

    def start_requests(self):
        queryfile = QUERYFILE
        fd = open(queryfile, 'rb')
        interface = self.start_urls[0]
        for line in fd.xreadlines():
            word = line
            if not word:
                continue
            else:
                option = [('num', 100), ("type", 2), ("query", word), ("tsn", 0)]
                option = urllib.urlencode(option)
                url = interface + option
                self.logger.info("*************************CRAWL URL****************************\n" + url)
                yield self.make_requests_from_url(url)
