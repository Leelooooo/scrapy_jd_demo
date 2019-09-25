# -*- coding: utf-8 -*-
"""
Created on 2019/9/23 11:03
@Author:lilu
@Desc: 脚本运行爬虫
"""
import logging
from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings
from scrapy.utils.log import configure_logging
from scrapy_jd_demo.utils.models import db_connect
from scrapy_jd_demo.utils.models import ProductRule
from sqlalchemy.orm import sessionmaker
from scrapy_jd_demo.spiders.jd_spider import FangtaiSpider

if __name__ == '__main__':
    settings = get_project_settings()
    configure_logging(settings)
    db = db_connect()
    Session = sessionmaker(bind=db)
    session = Session()
    rules = session.query(ProductRule).filter(ProductRule.enable == 1).all()
    session.close()
    runner = CrawlerRunner(settings)

    for rule in rules:
        # spider = ArticleSpider(rule)  # instantiate every spider using rule
        # stop reactor when spider closes
        # runner.signals.connect(spider_closing, signal=signals.spider_closed)
        runner.crawl(FangtaiSpider, rule=rule)

    d = runner.join()
    d.addBoth(lambda _: reactor.stop())

    # blocks process so always keep as the last statement
    reactor.run()
    logging.info('all finished.')