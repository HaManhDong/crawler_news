import datetime

import scrapy
from scrapy.exceptions import CloseSpider

from database import database_connection
from database.database_connection import NewsData


class NewspaperItem(scrapy.Item):
    url = scrapy.Field()
    title = scrapy.Field()
    summary = scrapy.Field()
    content = scrapy.Field()


class NewsItem:
    def __init__(self, url, title, summary, content):
        self.url = url
        self.title = title
        self.summary = summary
        self.content = content


class TuoiTreNewspaperSpider(scrapy.Spider):
    db_session = database_connection.connect_to_database()
    name = "TuoiTre"
    # start_urls = ['http://vnexpress.net/', ]
    start_urls = \
        [
            'http://tuoitre.vn', ]
    url_set = set(start_urls)

    crawled_page = 0

    def parse(self, response):
        news_title = TuoiTreNewspaperSpider.get_title(response)
        news_time = TuoiTreNewspaperSpider.get_time(response)
        summary = TuoiTreNewspaperSpider.get_summary(response)
        content = TuoiTreNewspaperSpider.get_content(response)
        url = response.url
        if news_title is not None and summary is not None and content is not None and news_time is not None:
            news_vn_express_data = NewsData(url=url, title=news_title, summary=summary, content=content,
                                            time=news_time)
            TuoiTreNewspaperSpider.db_session.add(news_vn_express_data)
            TuoiTreNewspaperSpider.db_session.commit()
        TuoiTreNewspaperSpider.crawled_page += 1
        if TuoiTreNewspaperSpider.crawled_page > 1000:
            raise CloseSpider('Search Exceeded 1000')
        next_link_list = []
        href_element = response.xpath("//*[starts-with(@href, 'http://tuoitre.vn')]")
        for link in href_element:
            link_url = link.xpath("./@href").extract_first()
            if link_url not in TuoiTreNewspaperSpider.url_set:
                TuoiTreNewspaperSpider.url_set.add(link_url)
                next_link_list.append(link_url)
        for next_link in next_link_list:
            yield scrapy.Request(next_link, callback=self.parse)
            # yield scrapy.Request(next_page, callback=self.parse)

            #
            # with open(filename, 'ab') as f:
            #     f.write()

    @staticmethod
    def get_title(response):
        news_title_element = response.xpath('//h1[@class="title-2"]/a/text()')
        if len(news_title_element) > 0:
            return news_title_element.extract_first()
        return None

    @staticmethod
    def get_summary(response):
        summary_element = response.xpath('//p[@class="txt-head"]/text()')
        if len(summary_element) > 0:
            return summary_element.extract_first()
        return None

    @staticmethod
    def get_content(response):
        content_block_element = response.xpath('//div[contains(@class,"fck")]')
        # if len(content_block_element) <= 0:
        #     content_block_element = response.xpath('//*[contains(@class,"block_content_slide_showdetail")]')
        if len(content_block_element) > 0:
            return_text = ''
            text_nodes = content_block_element[0].xpath(".//*[text()]")
            for text_node in text_nodes:
                return_text += text_node.xpath("./text()").extract_first()
            return return_text
        return None

    @staticmethod
    def get_time(response):
        # content_block_element =
        # response.xpath("//div[contains(@class, 'block_timer_share') and contains(@class, 'class2')]")
        content_block_element = response.xpath("//span[@class='date']/text()")
        if len(content_block_element) > 0:
            try:
                datetime_data = content_block_element.extract()[0].split(" ")
                date_data = datetime_data[0].split("/")
                time_data = datetime_data[1].split(":")
                if len(date_data) == 3 and len(time_data) == 2:
                    try:
                        check_date = datetime.datetime(
                            int(date_data[2]), int(date_data[1]), int(date_data[0]),
                            int(time_data[0]), int(time_data[1]))
                        return str(check_date.year) + '/' + str(check_date.month) + '/' + str(check_date.day) +\
                               '/' + str(check_date.hour) + '/' + str(check_date.minute)
                    except ValueError:
                        return None
            except Exception:
                return None
        return None


