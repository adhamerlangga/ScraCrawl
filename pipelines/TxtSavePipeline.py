import sqlite3
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(process)d - %(name)s - %(levelname)s - %(lineno)d -  %(message)s'
    )
logger = logging.getLogger('scrapme.pipelines.TxtSavePipeline')

class TxtSavePipeline(object):
    def __init__(self, file_name):
        logger.info('initialization')
        # Storing output filename
        self.file_name = file_name
        # Creating a file handle and setting it to None
        self.file_handle = None

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            file_name=crawler.settings.get('TXT_PATH'),
        )

    # def open_spider(self, spider):
    #     logger.info('spider open')

    #     # Opening file in binary-write mode
    #     file = open(self.file_name, 'wb')
    #     self.file_handle = file

    #     # Creating a FanItemExporter object and initiating export
    #     self.exporter = CsvItemExporter(file)
    #     self.exporter.start_exporting()
    
    # def close_spider(self, spider):
    #     logger.info('spider close')

    #     # Ending the export to file from FanItemExport object
    #     self.exporter.finish_exporting()

    #     # Closing the opened output file
    #     self.file_handle.close()
    
    def process_item(self, item, spider):
        logger.info('process item')

        with open(self.file_name, 'a+') as f:
            f.write("%s\n" % item)

        f.close() 
        # passing the item to FanItemExporter object for expoting to file
        # self.exporter.export_item(item)
        return item
