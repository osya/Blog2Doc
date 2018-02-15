#!/usr/bin/env python
# -*- coding: utf-8 -*-
from scrapy.item import Item, Field


class Post(Item):
    body = Field()
