from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from craigslist.spiders.craigslistspider import CraigslistspiderSpider

process = CrawlerProcess(get_project_settings())
process.crawl(CraigslistspiderSpider)
process.start()

