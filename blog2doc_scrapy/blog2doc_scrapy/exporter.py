#!/usr/bin/env python
# -*- coding: utf-8 -*-
from scrapy.exporters import BaseItemExporter
from blog2doc_scrapy.items import Page
from lxml import html, etree


class Blog2DocExporter(BaseItemExporter):
    page_tree = None
    content_node = None

    def __init__(self, file, **kwargs):
        super().__init__(**kwargs)
        self.file = file

    def export_item(self, item):
        if isinstance(item, Page):
            page_tree = etree.ElementTree(html.fromstring(item['body']))
            for node in page_tree.xpath('//*[not(descendant::*[contains(concat(" ", normalize-space(@class), " "), '
                                        '" post ")]) and not(ancestor::*[contains(concat(" ", normalize-space('
                                        '@class), " "), " post ")]) and ancestor::body]'):
                node.getparent().remove(node)
            self.page_tree = page_tree
            self.content_node = page_tree.xpath(".//*[@id='content']")[0]
        else:
            self.content_node.append(html.fromstring(item['body']))

    def finish_exporting(self):
        self.page_tree.write(self.file)
