from scrapy.crawler import CrawlerProcess
from us.usa_today.spider import UsaTodaySpider


process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
})

start_urls = ['http://www.usatoday.com/']
UsaTodaySpider.setup(start_urls, 'usa_today')

process.crawl(UsaTodaySpider)
process.start()  # the script will block here until the crawling is finished
