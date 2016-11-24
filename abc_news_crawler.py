from scrapy.crawler import CrawlerProcess
from us.abc_news.spider import ABCNewsSpider

process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
})
start_urls = ['http://abcnews.go.com']

ABCNewsSpider.setup(start_urls, 'abc_news')

process.crawl(ABCNewsSpider)
# process.crawl(TuoiTreNewspaperSpider)
# process.crawl(DanTriNewspaperSpider)
process.start()  # the script will block here until the crawling is finished
