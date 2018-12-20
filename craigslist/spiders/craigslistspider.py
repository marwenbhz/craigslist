# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.crawler import CrawlerProcess
from craigslist.items import CraigslistItem


class CraigslistspiderSpider(scrapy.Spider):
    name = 'craigslistspider'
    allowed_domains = ['craigslist.org']
    start_urls = ['https://boston.craigslist.org/search/egr']
    #custom_settings = {
    #'LOG_FILE': 'logs/craigslist.log',
    #'LOG_LEVEL':'INFO'
     #}

    def parse(self, response):

        print('PROCESSING...' + response.url)

	for job in response.css('li.result-row'):

	    try:
                title = job.css('a.result-title::text').extract() if len(job.css('a.result-title::text').extract()) != 0 else '-'
	    except:
		print('ERROR TITLE PARSE...' + response.url)
	    try:
		address = job.css('span.result-hood::text').extract() if len(job.css('span.result-hood::text').extract()) != 0 else '-'
	    except:
                print('ERROR ADRESSE PARSE...' + response.url)
	    try:
		url_page = job.css('a.result-title::attr(href)').extract_first() if len(job.css('a.result-title::attr(href)').extract_first()) != 0 else '-'
	    except:
                print('ERROR URL JOB PARSE...' + response.url)
	    try:
		publish_date = job.css('time.result-date::text').extract() if len(job.css('time.result-date::text').extract()) != 0 else '-'
	    except:
                print('ERROR PUBLICATION DATE PARSE...' + response.url)

	    yield Request(url_page, callback=self.parse_page, meta={'URL': url_page, 'Title': title, 'Address':address, 'publish_date':publish_date})

	relative_next_url = response.xpath('//a[@class="button next"]/@href').extract_first()
        absolute_next_url = response.urljoin(relative_next_url)
        yield Request(absolute_next_url, callback=self.parse)



    def parse_page(self, response):

        item = CraigslistItem()

        item['JOB_URL'] = response.meta.get('URL')
        item['JOB_TITLE'] = response.meta.get('Title')
        item['ADRESSE'] = response.meta.get('Address')
        item['PUBLICATION_DATE'] = response.meta.get('publish_date')

	# Don't need to add description in our output, if you need description of job, just uncomment this code and uncomment description field in items.py.
	#try:
	#    item['DESCRIPTION'] = "".join(line for line in response.xpath('//*[@id="postingbody"]/text()').extract()).strip()
	#except:
	#    print('ERROR DESCRIPTION PARSE...' + response.url)

	try:
	    item['JOB_ID'] = response.css('div.postinginfos > p::text').extract_first()[9::]
	except:
	    print('ERROR JOB ID PARSE...' + response.url)


	keys = response.css('p.attrgroup > span::text').extract()
	if len(keys) == 1:
	    try:
	        item['COMPENSATION'] = response.css('p.attrgroup > span > b::text ').extract()[0] if keys[0] == 'compensation: ' else '-'
	    except:
		print('ERROR COMPENSATION PARSE...' + response.url)
	    try:
		item['EMPLOYMENT_TYPE'] = response.css('p.attrgroup > span > b::text ').extract()[0] if keys[0] == 'employment type: ' else '-'
	    except:
		print('ERROR EMPLOYEMENT TYPE PARSE...' + response.url)
	else:
	    try:
		item['COMPENSATION'] = response.css('p.attrgroup > span > b::text ').extract()[0] if keys[0] == 'compensation: ' else '-'
            except:
		print('ERROR COMPENSATION PARSE...' + response.url)
	    try:
		item['EMPLOYMENT_TYPE'] = response.css('p.attrgroup > span > b::text ').extract()[1] if keys[1] == 'employment type: ' else '-'
            except:
                print('ERROR EMPLOYEMENT TYPE PARSE...' + response.url)

	yield item

