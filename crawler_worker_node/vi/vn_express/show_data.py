# import scrapy
# from scrapy.crawler import CrawlerProcess
from database import database_connection
from database.database_connection import NewsData


def show_news_list():
    db_session = database_connection.connect_to_database()
    # news_list = db_session.query(VnExpressData).filter_by(name='ed')
    news_list = db_session.query(NewsData).all()
    for x in news_list:
        print(x)


show_news_list()
