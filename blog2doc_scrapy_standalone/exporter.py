#!/usr/bin/env python
# -*- coding: utf-8 -*-
from scrapy.exporters import BaseItemExporter


class Blog2DocExporter(BaseItemExporter):
    def __init__(self, **kwargs):
        pass
        # TODO: open file

    def finish_exporting(self):
        # TODO: close file
        pass

    def export_item(self, item):
        pass
