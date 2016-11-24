from scrapy.crawler import CrawlerProcess
from us.telegraph.spider import TelegraphSpider

process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
})
start_urls = ['http://www.telegraph.co.uk/']

TelegraphSpider.setup(start_urls, 'telegraph')

process.crawl(TelegraphSpider)
# process.crawl(TuoiTreNewspaperSpider)
# process.crawl(DanTriNewspaperSpider)
process.start()  # the script will block here until the crawling is finished
