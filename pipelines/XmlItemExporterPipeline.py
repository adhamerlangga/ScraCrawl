# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.exporters import XmlItemExporter

# https://stackoverflow.com/questions/41066481/how-to-set-crawler-parameter-from-scrapy-spider
class XmlItemExporterPipeline(object):

    def __init__(self, file_name):
        # Storing output filename
        self.file_name = file_name
        # Creating a file handle and setting it to None
        self.file_handle = None

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            file_name=crawler.settings.get('XML_PATH'),
        )


    def open_spider(self, spider):
        print('Custom export opened')

        # Opening file in binary-write mode
        file = open(self.file_name, 'wb')
        self.file_handle = file

        # Creating a FanItemExporter object and initiating export
        self.exporter = XmlItemExporter(file)
        self.exporter.start_exporting()
    
    def close_spider(self, spider):
        print('Custom Exporter closed')

        # Ending the export to file from FanItemExport object
        self.exporter.finish_exporting()

        # Closing the opened output file
        self.file_handle.close()
    
    def process_item(self, item, spider):
        # passing the item to FanItemExporter object for expoting to file
        self.exporter.export_item(item)
        return item
