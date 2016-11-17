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


class DanTriNewspaperSpider(scrapy.Spider):
    db_session = database_connection.connect_to_database()
    name = "DanTri"
    # start_urls = ['http://vnexpress.net/', ]
    start_urls = \
        [
            'http://dantri.com.vn', ]
    url_set = set(start_urls)
    url_start_set = {'xa-hoi', 'su-kien', 'the-gioi', 'the-thao', 'giao-duc-khuyen-hoc', 'tam-long-nhan-ai',
                     'kinh-doanh', 'van-hoa', 'giai-tri', 'phap-luat'}
    crawled_page = 0

    def parse(self, response):
        news_title = DanTriNewspaperSpider.get_title(response)
        news_time = DanTriNewspaperSpider.get_time(response)
        summary = DanTriNewspaperSpider.get_summary(response)
        content = DanTriNewspaperSpider.get_content(response)
        url = response.url
        if news_title is not None and summary is not None and content is not None and news_time is not None:
            news_vn_express_data = NewsData(url=url, title=news_title, summary=summary, content=content,
                                            time=news_time)
            DanTriNewspaperSpider.db_session.add(news_vn_express_data)
            DanTriNewspaperSpider.db_session.commit()
        DanTriNewspaperSpider.crawled_page += 1
        if DanTriNewspaperSpider.crawled_page > 1000:
            raise CloseSpider('Search Exceeded 1000')
        next_link_list = []
        href_element_list = []
        for content in DanTriNewspaperSpider.url_start_set:
            href_element_list.append(response.xpath('//a[contains(@href,"' + content + '")]'))
        for href_element in href_element_list:
            for link in href_element:
                link_url = 'http://dantri.com.vn' + link.xpath("./@href").extract_first()
                if link_url not in DanTriNewspaperSpider.url_set:
                    DanTriNewspaperSpider.url_set.add(link_url)
                    next_link_list.append(link_url)
        for next_link in next_link_list:
            yield scrapy.Request(next_link, callback=self.parse)
            # yield scrapy.Request(next_page, callback=self.parse)

            #
            # with open(filename, 'ab') as f:
            #     f.write()

    @staticmethod
    def get_title(response):
        news_title_element = response.xpath("//h1[contains(@class, 'fon31') and contains(@class, 'mgb15')]/text()")
        if len(news_title_element) > 0:
            return news_title_element.extract_first()
        return None

    @staticmethod
    def get_summary(response):
        summary_element = response.xpath("//h2[contains(@class, 'fon33')]/text()").extract()
        if len(summary_element) > 0:
            return_summary = ''
            for text in summary_element:
                return_summary += text
            return return_summary
        return None

    @staticmethod
    def get_content(response):
        content_block_element = response.xpath('//div[@id="divNewsContent"]')
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
        # content_block_element =fr fon7 mr2 tt-capitalize
        # response.xpath("//div[contains(@class, 'block_timer_share') and contains(@class, 'class2')]")
        content_block_element = response.xpath("//span[contains(@class, 'fr') and contains(@class, 'fon7')"
                                               "and contains(@class, 'mr2') and contains(@class, 'tt-capitalize')]"
                                               "/text()")
        if len(content_block_element) > 0:
            try:
                datetime_data = content_block_element.extract()[0].split(" ")
                date_data = []
                time_data = []
                for content in datetime_data:
                    if has_numbers(content) and "/" in content:
                        date_data = content.split("/")
                    if has_numbers(content) and ":" in content:
                        time_data = content.split(":")
                if len(date_data) == 3 and len(time_data) == 2:
                    try:
                        check_date = datetime.datetime(
                            int(date_data[2]), int(date_data[1]), int(date_data[0]),
                            int(time_data[0]), int(time_data[1]))
                        return str(check_date.year) + '/' + str(check_date.month) + '/' + str(check_date.day) + \
                               '/' + str(check_date.hour) + '/' + str(check_date.minute)
                    except ValueError:
                        return None
            except Exception:
                return None
        return None


def has_numbers(input_string):
    return any(char.isdigit() for char in input_string)
