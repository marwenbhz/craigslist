# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CraigslistItem(scrapy.Item):
    # define the fields for your item here like:
    JOB_TITLE = scrapy.Field()
    ADRESSE = scrapy.Field()
    PUBLICATION_DATE = scrapy.Field()
    JOB_URL = scrapy.Field()
    #DESCRIPTION = scrapy.Field()
    COMPENSATION = scrapy.Field()
    EMPLOYMENT_TYPE = scrapy.Field()
    JOB_ID = scrapy.Field()
