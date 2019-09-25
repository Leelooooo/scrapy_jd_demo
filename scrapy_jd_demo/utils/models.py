"""
Created on 2019/9/23 10:43
@Author:lilu
@Desc: 定义数据库模型实体
"""


from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.engine.url import URL
from sqlalchemy.ext.declarative import declarative_base

from scrapy_jd_demo.settings import DATABASE


def db_connect():
    """
    Performs database connection using database settings from settings.py.
    Returns sqlalchemy engine instance
    """
    return create_engine(URL(**DATABASE))

def create_news_table(engine):
    Base.metadata.create_all(engine)

Base = declarative_base()


class ProductRule(Base):
    """自定义产品爬取规则"""
    __tablename__ = 'product_rule'

    id = Column(Integer, primary_key=True)
    name = Column(String(30))
    allow_domains = Column(String(100))
    start_urls = Column(String(100))
    next_page = Column(String(100))
    allow_url = Column(String(200))
    product_name = _xpath = Column(String(200))
    product_price_xpath = Column(String(200))
    product_comment_num_xpath = Column(String(200))
    product_shop_xpath = Column(String(200))
    enable = Column(Integer)


class Product(Base):
    """产品类"""
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    url = Column(String(100))
    name = Column(String(100))
    price = Column(String(100))
    comment_num = Column(String(100))
    shop = Column(String(100))
