# import io
# import re
import PyPDF2
import scrapy
# from scrapy.item import Item
import pathlib
import os
from io import BytesIO

class PdfSpider(scrapy.Spider):
    name = "pdf"
    start_urls = [
        pathlib.Path(os.path.abspath('pdf_folder/instagram.pdf')).as_uri()]
    
    # custom_settings = {
    #     'FEED_URI' : 'pdf.json',
    #     }   
    
    def parse(self, response):
        self.logger.info('A response from %s just arrived!', response.url)
        stream = BytesIO(response.body)
        reader = PyPDF2.PdfFileReader(stream)

        text = u""

        # if reader.getDocumentInfo().title:
        #         # Title is optional, may be None
        #         text += reader.getDocumentInfo().title

        for page in reader.pages:
                # XXX: Does handle unicode properly?
                text += page.extractText()
                yield {'content': text}

        # yield{'test': response.body}