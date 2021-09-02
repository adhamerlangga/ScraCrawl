import scrapy

class Author(scrapy.Item):
    name = scrapy.Field()
    birthday = scrapy.Field()
    bio = scrapy.Field()
    last_updated = scrapy.Field(serializer=str)