#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
from lxml import html
from pathlib import Path
import docx
import win32com.client

DATA_URL = 'http://exampleofablog.com/'
DATA_DIR = Path(Path.cwd().parent, 'data')


class CMain(object):
    url = ''

    def __init__(self, url):
        self.url = url

    def run(self):
        page = requests.get(self.url)
        tree = html.fromstring(page.content)
        out_tree = None
        content_node = None
        for i, link in enumerate(tree.xpath(".//article/header/hgroup/h2/a/@href")):
            post = requests.get(link)
            post_tree = html.fromstring(post.content)

            if 0 == i:
                for node in post_tree.xpath(
                        '//*[not(descendant::*[contains(concat(" ", normalize-space(@class), " "), " post ")]) and not('
                        'ancestor-or-self::*[contains(concat(" ", normalize-space(@class), " "), " post ")]) and '
                        'ancestor::body]'):
                    node.getparent().remove(node)
                out_tree = post_tree
                content_node = out_tree.xpath(".//*[@id='content']")[0]
            else:
                node = post_tree.xpath('.//*[contains(concat(" ", normalize-space(@class), " "), " post ")]')[0]
                content_node.append(node)

        page_file_name = Path(DATA_DIR, f'page.html')
        with open(page_file_name, 'wb') as file:
            file.write(html.tostring(out_tree, encoding='unicode').encode('utf-8'))




                # posts = tree.xpath('.//*[contains(concat(" ", normalize-space(@class), " "), " post ")]')
                # for i, post in enumerate(posts):
                #     with open(Path(DATA_DIR, f'post_{i}.html'), 'wb') as file:
                #         file.write(html.tostring(post, encoding='unicode').encode('utf-8'))

                # word = win32com.client.Dispatch('Word.Application')
                # doc = word.Documents.Add(page_file_name)
                # # doc.SaveAs(Path(DATA_DIR, 'page.docx'), FileFormat=0)
                # doc.Close()
                # word.Quit()


CMain(DATA_URL).run()

# TODO: Видео некорректно вставляется
# TODO: переписать это все на Scrapy для асинхронности
