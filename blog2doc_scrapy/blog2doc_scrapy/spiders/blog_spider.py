# -*- coding: utf-8 -*-
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from blog2doc_scrapy.items import Post, Page


class BlogSpiderSpider(CrawlSpider):
    name = "blog_spider"
    allowed_domains = ["exampleofablog.com"]
    start_urls = ['http://exampleofablog.com/']
    rules = (
        Rule(LinkExtractor(restrict_xpaths=('.//article/header/hgroup/h2/a',)), callback='parse_page', follow=True),
        Rule(LinkExtractor(restrict_xpaths=('.//*[contains(concat(" ", normalize-space(@class), " "), '
                                            '" pagination_container ")]/nav/*[contains(concat(" ", normalize-space('
                                            '@class), " "), " current ")]/following-sibling::a[1]',)), follow=True),
             )

    def __init__(self, *a, **kw):
        super().__init__(*a, **kw)
        self.header_and_footer_generate = False

    @staticmethod
    def parse_page(response):
        post_node = \
            (response.xpath('.//*[contains(concat(" ", normalize-space(@class), " "), " post ")][1]') or [None])[0]
        if post_node is not None:
            item = Post()
            item['url'] = response.url
            item['body'] = post_node.extract()
            yield item

    def parse_start_url(self, response):
        item = Page()
        item['url'] = response.url
        item['body'] = response.text
        self.header_and_footer_generate = True
        return item
