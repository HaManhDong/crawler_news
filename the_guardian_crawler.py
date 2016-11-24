from scrapy.crawler import CrawlerProcess
from us.the_guardian.spider import TheGuardianSpider

process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
})
start_urls = ['https://www.theguardian.com/business/2016/aug/12/airing-the-imfs-dirty-european-laundry']

TheGuardianSpider.setup(start_urls, 'the_guarian')

process.crawl(TheGuardianSpider)
# process.crawl(TuoiTreNewspaperSpider)
# process.crawl(DanTriNewspaperSpider)
process.start()  # the script will block here until the crawling is finished
