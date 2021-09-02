# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field
from scrapy.loader.processors import MapCompose, TakeFirst
class FileItem(Item):
    header = Field(
        input_processor=MapCompose(str.strip),
        output_processor=TakeFirst()
        )
    url = Field(
        input_processor=MapCompose(str.strip),
        output_processor=TakeFirst()
        )
    images = Field(
        input_processor=MapCompose(str.strip),
        output_processor=TakeFirst()
    )
    image_urls = Field(
        input_processor=MapCompose(str.strip),
        output_processor=TakeFirst()
    )
    files = Field(
        input_processor=MapCompose(str.strip),
        output_processor=TakeFirst()
        )
    file_urls = Field(
        input_processor=MapCompose(str.strip),
        output_processor=TakeFirst()
        )
