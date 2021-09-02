from scrapy.item import Item, Field
from scrapy.loader.processors import MapCompose, TakeFirst
class SpringerBookItem(Item):
    title = Field(
        input_processor=MapCompose(str.strip),
        output_processor=TakeFirst()
        )
    first_author_name = Field(
        input_processor=MapCompose(str.strip),
        output_processor=TakeFirst()
        )
    doi = Field(
        input_processor=MapCompose(str.strip),
        output_processor=TakeFirst()
        )
    copyright_info = Field(
        input_processor=MapCompose(str.strip),
        output_processor=TakeFirst()
        )
    publisher_name = Field(
        input_processor=MapCompose(str.strip),
        output_processor=TakeFirst()
        )
    print_isbn = Field(
        input_processor=MapCompose(str.strip),
        output_processor=TakeFirst()
        )
    electronic_isbn = Field(
        input_processor=MapCompose(str.strip),
        output_processor=TakeFirst()
        )
    file_urls = Field(
        input_processor=MapCompose(str.strip),
        output_processor=TakeFirst()
    )
    files = Field(
        input_processor=MapCompose(str.strip),
        output_processor=TakeFirst()
    )
