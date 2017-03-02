# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field


class Post(Item):
    url = Field()
    body = Field()


class Page(Item):
    """
     This item contains page for generate header and footer from it
    """
    url = Field()
    body = Field()
