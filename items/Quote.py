import scrapy

class Quote(scrapy.Item):
    text = scrapy.Field()
    author = scrapy.Field()
    tags = scrapy.Field()
    last_updated = scrapy.Field(serializer=str)