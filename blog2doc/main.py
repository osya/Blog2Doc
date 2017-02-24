#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
from lxml import html
from pathlib import Path
import copy

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
            self.cur_page_tree = html.parse(next_link)
            self.page_num += 1
            return True
        else:
            return False

    def process_page(self):
        if self.out_tree is None:
            self.out_tree = copy.deepcopy(self.cur_page_tree)
            for node in self.out_tree.xpath('//*[not(descendant::*[contains(concat(" ", normalize-space(@class), '
                                            '" "), " post ")]) and not(ancestor::*[contains(concat(" ", '
                                            'normalize-space(@class), " "), " post ")]) and ancestor::body]'):
                node.getparent().remove(node)
            self.content_node = self.out_tree.xpath(".//*[@id='content']")[0]

        for i, link in enumerate(self.cur_page_tree.xpath(".//article/header/hgroup/h2/a/@href")):
            post = requests.get(link)
            post_tree = html.fromstring(post.content)
            node = post_tree.xpath('.//*[contains(concat(" ", normalize-space(@class), " "), " post ")]')[0]
            self.content_node.append(node)

    def save_blog(self):
        file_name = Path(DATA_DIR, f'blog.html')
        self.out_tree.write(str(file_name))

    def run(self):
        while self.next():
            self.process_page()
        self.save_blog()

CMain(DATA_URL).run()
