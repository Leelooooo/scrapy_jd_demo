# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html
import random

from fake_useragent import UserAgent
from scrapy import signals
from scrapy_jd_demo.settings import PROXIES


# IP proxy
class ProxyMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    def __init__(self, ip=""):
        self.ip = ip

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader middleware.
        proxy = random.choice(PROXIES)
        print("当前使用的IP为： " + proxy["ipaddr"])
        request.meta["proxy"] = "https://" + proxy["ipaddr"]

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


# fake_useragent
class UserAgentMiddlware(object):
    # random user-agent
    def __init__(self, crawler):
        super(UserAgentMiddlware, self).__init__()
        self.ua = UserAgent()
        self.ua_type = crawler.settings.get('RANDOM_UA_TYPE', 'random')  # 从setting文件中读取RANDOM_UA_TYPE值

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    def process_request(self, request, spider):  ###系统电泳函数
        def get_ua():
            return getattr(self.ua, self.ua_type)

        user_agent_random = get_ua()
        print("当前使用的User-Agent是： " + user_agent_random)
        request.headers.setdefault('User_Agent', user_agent_random)
        pass


class ScrapyJdDemoSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
