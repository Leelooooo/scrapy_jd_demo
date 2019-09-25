# -*- coding: utf-8 -*-
"""
Created on 2019/9/23 10:57
@Author:lilu
@Desc: 
"""
from contextlib import contextmanager

from sqlalchemy.orm import sessionmaker

from scrapy_jd_demo.utils.models import db_connect, create_news_table, ProductRule


@contextmanager
def session_scope(Session):
    """Provide a transactional scope around a series of operations."""
    session = Session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()

def init_rule():
    engine = db_connect()
    create_news_table(engine)
    Session = sessionmaker(bind=engine)
    with session_scope(Session) as session:
        product_rule1 = ProductRule(
            name='huxiu',
            allow_domains='huxiu.com',
            start_urls='http://www.huxiu.com/',
            next_page='',
            allow_url='/article/\d+/\d+\.html',
            extract_from='//div[@class="mod-info-flow"]',
            title_xpath='//div[@class="article-wrap"]/h1/text()',
            body_xpath='//div[@id="article_content"]/p//text()',
            publish_time_xpath='//span[@class="article-time"]/text()',
            source_site='虎嗅网',
            enable=1
        )
        product_rule2 = ProductRule(
            name='osc',
            allow_domains='oschina.net',
            start_urls='http://www.oschina.net/',
            next_page='',
            allow_url='/news/\d+/',
            extract_from='//div[@id="IndustryNews"]',
            title_xpath='//h1[@class="OSCTitle"]/text()',
            publish_time_xpath='//div[@class="PubDate"]/text()',
            body_xpath='//div[starts-with(@class, "Body")]/p[position()>1]//text()',
            source_site='开源中国',
            enable=1
        )
        session.add(product_rule1)
        session.add(product_rule2)
