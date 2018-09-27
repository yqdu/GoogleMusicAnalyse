# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
class GoogleItem(scrapy.Item):
    Url = scrapy.Field()
    Name = scrapy.Field()
    category = scrapy.Field()
    Review_number = scrapy.Field()
    Rating=scrapy.Field()
    Price=scrapy.Field()
    Duration = scrapy.Field()
    Released=scrapy.Field()
    Label=scrapy.Field()
    Tracks=scrapy.Field()



class ApptestItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass
