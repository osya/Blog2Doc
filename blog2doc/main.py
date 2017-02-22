#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
from lxml import html
from pathlib import Path

DATA_URL = 'http://exampleofablog.com/'
DATA_DIR = Path(Path.cwd().parent, 'data')


class CMain(object):
    url = None
    cur_page_tree = None
    page_num = 0
    out_tree = None
    content_node = None

    def __init__(self, url):
        self.url = url

    def next(self):
        next_link = (self.cur_page_tree.xpath('.//*[contains(concat(" ", normalize-space(@class), " "), '
                                              '" pagination_container ")]/nav/*[contains(concat(" ", normalize-space('
                                              '@class), " "), " current ")]/following-sibling::a[1]/@href') or [
                         None])[0] if self.cur_page_tree is not None else self.url
        if next_link is not None:
            page = requests.get(next_link)
            self.cur_page_tree = html.fromstring(page.content)
            self.page_num += 1
            return True
        else:
            return False

    def process_page(self):
        for i, link in enumerate(self.cur_page_tree.xpath(".//article/header/hgroup/h2/a/@href")):
            post = requests.get(link)
            post_tree = html.fromstring(post.content)
            if self.out_tree is None:
                for node in post_tree.xpath(
                        '//*[not(descendant::*[contains(concat(" ", normalize-space(@class), " "), " post ")]) and not('
                        'ancestor-or-self::*[contains(concat(" ", normalize-space(@class), " "), " post ")]) and '
                        'ancestor::body]'):
                    node.getparent().remove(node)
                self.out_tree = post_tree
                self.content_node = self.out_tree.xpath(".//*[@id='content']")[0]
            else:
                node = post_tree.xpath('.//*[contains(concat(" ", normalize-space(@class), " "), " post ")]')[0]
                self.content_node.append(node)

    def save_blog(self):
        file_name = Path(DATA_DIR, f'blog.html')
        with open(file_name, 'wb') as file:
            file.write(html.tostring(self.out_tree, encoding='unicode').encode('utf-8'))

    def run(self):
        while self.next():
            self.process_page()
        self.save_blog()

CMain(DATA_URL).run()

# TODO: переписать это все на Scrapy для асинхронности. Сравнить скорость загрузки всего блога в Scrapy и без Scrapy
