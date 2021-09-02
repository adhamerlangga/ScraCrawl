from scrapy.exporters import BaseItemExporter
from scrapy.exporters import XmlItemExporter
from scrapy.exporters import PythonItemExporter
from scrapy.exporters import CsvItemExporter
from scrapy.exporters import PickleItemExporter
from scrapy.exporters import PprintItemExporter
from scrapy.exporters import JsonItemExporter
from scrapy.exporters import JsonLinesItemExporter
from scrapy.exporters import MarshalItemExporter

class PerYearXmlExportPipeline(object):
    """Distribute items across multiple XML files according to their 'year' field"""

    def open_spider(self, spider):
        self.year_to_exporter = {}

    def close_spider(self, spider):
        for exporter in self.year_to_exporter.values():
            exporter.finish_exporting()

    def _exporter_for_item(self, item):
        year = item['year']
        if year not in self.year_to_exporter:

            f = open('{}.xml'.format(year), 'wb')
            # f = open('{}.py'.format(year), 'wb')
            # f = open('{}.csv'.format(year), 'wb')
            # f = open('{}.pickle'.format(year), 'wb')
            # f = open('{}.json'.format(year), 'wb')
            # f = open('{}.jl'.format(year), 'wb')
            # f = open('{}.marshal'.format(year), 'wb')

            exporter = XmlItemExporter(f)
            # exporter = BaseItemExporter(f)
            # exporter = PythonItemExporter(f)
            # exporter = CsvItemExporter(f)
            # exporter = PickleItemExporter(f)
            # exporter = PprintItemExporter(f)
            # exporter = JsonItemExporter(f)
            # exporter = JsonLinesItemExporter(f)
            # exporter = MarshalItemExporter(f)
            exporter.start_exporting()
            self.year_to_exporter[year] = exporter
        return self.year_to_exporter[year]

    def process_item(self, item, spider):
        exporter = self._exporter_for_item(item)
        exporter.export_item(item)
        return item