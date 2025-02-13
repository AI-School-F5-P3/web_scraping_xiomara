# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class QuoteItem(scrapy.Item):
    # define the fields for your item here like:
    quote = scrapy.Field()
    author = scrapy.Field()
    tags = scrapy.Field()

class AuthorItem(scrapy.Item):
    author = scrapy.Field()
    about = scrapy.Field()