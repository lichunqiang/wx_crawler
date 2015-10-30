# -*- coding: utf-8 -*-
from scrapy import log
from proxy import PROXIES
from agents import AGENTS

import random

class CustomHttpProxyMiddleware(object):

	def process_request(self, request, spider):
		if self.use_proxy(request):
			p = random.choice(PROXIES)
			try:
				request.meta['proxy'] = "http://%s" % p['ip_port']
			except Exception, e:
				log.msg("Exception %s" % e, _level = log.CRITICAL)

	def use_proxy(self, request):
		"""
		using direct download for depth <= 2
		using proxy with probability 0.3
		"""
		if "depth" in request.meta and int(request.meta['depth']) <= 2:
			return False
		i = random.randint(1, 10)
		return i <= 2

class CustomUserAgentMiddleware(object):
	"""
	the middleware for random user agent
	"""
	def process_request(self, request, spider):
		agent = random.choice(AGENTS)
		request.headers['User-Agent'] = agent
