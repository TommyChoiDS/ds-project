# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class SkEncarItem(scrapy.Item):
    # define the fields for your item here like:
    Manufacturer = scrapy.Field()
    Model = scrapy.Field()
    Km = scrapy.Field()
    Fuel = scrapy.Field()
    Loc = scrapy.Field()
    Price = scrapy.Field()
    Old_year = scrapy.Field()
    Old_month = scrapy.Field()
    pass
