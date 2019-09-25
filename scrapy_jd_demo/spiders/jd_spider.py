from scrapy import Spider
from scrapy_splash import SplashRequest

from scrapy_jd_demo.items import ScrapyJdDemoItem


class JdSpider(Spider):
    name = "jd_spider"
    # headers = {
    #     'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'}
    start_urls = [
        "https://list.jd.com/list.html?cat=737,13297,13881&sort=sort_rank_asc&trans=1&ev=exbrand_6706&JL=3_%E5%93%81%E7%89%8C_%E6%96%B9%E5%A4%AA%EF%BC%88FOTILE%EF%BC%89#J_crumbsBar",
        "https://list.jd.com/list.html?cat=737,13297,13881&ev=exbrand_55546&sort=sort_rank_asc&trans=1&JL=2_1_0#J_crumbsBar"
    ]

    def start_requests(self):
        splash_args = {
            'wait': 0.5,
        }
        for url in self.start_urls:
            yield SplashRequest(url=url, callback=self.parse_result, endpoint='render.html', args=splash_args,
                                splash_headers=None)

    def parse_result(self, response):
        # debuging on command line
        # from scrapy.shell import inspect_response
        # inspect_response(response, self)

        item = ScrapyJdDemoItem()
        products = response.xpath('//ul[@class="gl-warp clearfix"]/li')
        for product in products:
            item['name'] = product.xpath('.//div[@class="p-name"]/a/em/text()').extract()[0].strip()
            item['price'] = product.xpath('.//div[@class="p-price"]/strong/i/text()').extract_first()
            item['comment_num'] = product.xpath('.//div[@class="p-commit p-commit-n"]/strong/a/text()').extract()[
                0].strip()
            item['shop'] = product.xpath('.//div[@class="p-shop"]/span/a/text()').extract()[0].strip()
            yield item

        sub_next_url = response.xpath('//a[@class="pn-next"]/@href').extract()
        if sub_next_url:
            next_url = 'https://list.jd.com' + sub_next_url[0]
            splash_args = {
                'wait': 0.5,
            }
            yield SplashRequest(url=next_url, callback=self.parse_result, endpoint='render.html', args=splash_args,
                                splash_headers=None)
