import logging

import scrapy
import scrapy_splash
from scrapy_splash import SplashRequest


class JsSpider(scrapy.Spider):
    name = "jd"
    # headers = {
    #     'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'}
    start_urls = [
        "https://list.jd.com/list.html?cat=737,13297,13881&sort=sort_rank_asc&trans=1&ev=exbrand_6706&JL=3_%E5%93%81%E7%89%8C_%E6%96%B9%E5%A4%AA%EF%BC%88FOTILE%EF%BC%89#J_crumbsBar"
    ]

    def start_requests(self):
        # splash_args = {
        #     # optional; parameters passed to Splash HTTP API
        #     'wait': 0.5,
        #     # 'url' is prefilled from request url
        #     # 'http_method' is set to 'POST' for POST requests
        #     # 'body' is set to request body for POST requests
        # }
        for url in self.start_urls:
            # 方式1：调用SplashRequest发送请求
            # yield SplashRequest(url=url, callback=self.parse, endpoint='render.html', args=splash_args,
            #                     splash_headers=self.headers)

            # 方式2：调用常规scrapy.Request发送请求，传入meta['Splash']启动Splash
            yield scrapy.Request(url, self.parse, meta={
                'splash': {
                    # 这里设置渲染参数
                    'args': {
                        'wait': 0.5
                        # 'url' 是由请求url预填的
                        # 对于POST请求, 'http_method'设置为'POST'
                        # 'body'被设置为请求POST请求的主体
                    },

                    # 可选参数
                    'endpoint': 'render.html',  # 可选; 默认为 render.json
                    # 'splash_headers': False,  # 可选; 发送给Splash服务器的一个dict类型的headers，不是发往远程web站点的HTTP头部
                    'dont_send_headers': True,
                }
            })

    def parse(self, response):
        logging.info(u'----------使用splash爬取京东网首页异步加载内容-----------')

        name = response.xpath('.//div[@class="p-name"]/a/em/text()').extract()[0].strip()
        price = response.xpath('.//div[@class="p-price"]/strong/i/text()').extract()[0]
        comment_num = response.xpath('.//div[@class="p-commit p-commit-n"]/strong/a/text()').extract()[0]
        shop = response.xpath('.//div[@class="p-shop"]/span/a/text()').extract()[0]

        logging.info(u"find name：%s" % name)
        logging.info(u"find price：%s" % price)
        logging.info(u"find comment_num：%s" % comment_num)
        logging.info(u"find shop：%s" % shop)
        logging.info(u'---------------success----------------')
