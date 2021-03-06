from misc.proxy import PROXIES
from misc.agents import AGENTS

import urllib2
import json
import random
import logging

logger = logging.getLogger(__name__)
"""
Custom proxy provider.
"""

class CustomHttpProxyMiddleware(object):
    MIN_NUM_PROXY = 10

    def __init__(self):
        self.proxies = self.__getproxies__()
        self.anti = []
        self.bad = []

    def __zhengli__(self, proxies):
        result = []
        pxy = {}
        for proxy in proxies:
            key = str(proxy[u'ip'])
            pxy[key].append(proxy) if pxy.has_key(key) else pxy.update({key:[proxy,]})

            sorted(pxy[key], lambda x,y: cmp(x['speed'] , y['speed']))

        for item in pxy.values():
            result.append(item[0])

        return result

    def __getproxies__(self):
        PROXY_SERVICE = r"http://172.16.80.64:50000/select?num=500&speed=0.5"

        data = urllib2.urlopen(PROXY_SERVICE).read()
        proxies = json.loads(data)['ips']

        pxy = self.__zhengli__(proxies)
        res = []
        for proxy in pxy:
            ip_port = {'ip_port': "http://" + str(proxy[u'ip']) + ":" + str(proxy[u'port'])}
            res.append(ip_port)

        return res

    def process_request(self, request, spider):
        # TODO implement complex proxy providing algorithm
        if len(self.proxies) < self.MIN_NUM_PROXY:
            logger.info("The volume of proxy-pool is ******LOW******. Now reload proxy-pool.")
            self.proxies = self.__getproxies__()
            logger.info("Reload proxies successfully.Now there are %s proxies." %len(self.proxies))

        p = random.choice(self.proxies)
        try:
            request.meta['proxy'] = p['ip_port']
            logger.debug("Add proxy %s" % p['ip_port'])
        except Exception, e:
            logger.debug("Exception %s" % e)


    def process_response(self, request, response, spider):

        logger.info("Response Status code is : %s." %repr(response.status))
        logger.info("Response Headers is :\n %s." %repr(response.headers))
        if response.status == 302 and "Location" in response.headers:
            proxy = request.meta.pop('proxy')
            self.proxies.remove({'ip_port': proxy})
            self.anti.append({'ip_port': proxy})
            logger.info("Proxy %s has been ******ANTIED******, remove it." %proxy)
            logger.info("Retry the request %s." %request.url)
            logger.info("Original request is %s" %request.url)
            logger.info("Response request is %s" %repr(response.request))
            return request
        elif response.status == 404:
            proxy = request.meta.pop('proxy')
            self.proxies.remove({'ip_port': proxy})
            self.anti.append({'ip_port': proxy})
            logger.info("Proxy %s is ******NOT WORK******, remove it." %proxy)
            logger.info("Retry the request %s." %request.url)
            logger.info("Original request is %s" %request.url)
            logger.info("Response request is %s" %repr(response.request))
            return request
        elif response.status in [403,]:
            proxy = request.meta.pop('proxy')
            self.proxies.remove({'ip_port': proxy})
            self.anti.append({'ip_port': proxy})
            logger.info("Proxy %s has been ******FORBIDDEN******, remove it." %proxy)
            logger.info("Retry the request %s." %request.url)
            logger.info("Original request is %s" %request.url)
            logger.info("Response request is %s" %repr(response.request))
            return request
        elif response.status in [500, 501, 502, 503, 504, 505]:
            proxy = request.meta.pop('proxy')
            self.proxies.remove({'ip_port': proxy})
            self.anti.append({'ip_port': proxy})
            logger.info("Proxy %s is ******NOT WORK******, remove it." %proxy)
            logger.info("Retry the request %s." %request.url)
            logger.info("Original request is %s" %request.url)
            logger.info("Response request is %s" %repr(response.request))
            return request

        else:
            return response

    def process_exception(self, request, exception, spider):
        logger.info("Catch a Exception: ******%s******" %repr(exception))
        logger.info("request is %s" %request.url)
        if request.meta.has_key('proxy'):
            proxy = request.meta.pop('proxy')
        if proxy:
            self.proxies.remove({'ip_port': proxy})
            self.bad.append({'ip_port': proxy})
            logger.info("Proxy %s cannot ******REACHED******, remove it." %proxy)
            logger.info("Retry the request %s." %request.url)
        return request

"""
change request header nealy every time
"""
class CustomUserAgentMiddleware(object):
    def process_request(self, request, spider):
        agent = random.choice(AGENTS)
        request.headers['User-Agent'] = agent
        logger.debug("Add agent %s" % agent)
