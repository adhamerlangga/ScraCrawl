import scrapy

class UserAgentSpider(scrapy.Spider):
    name = 'user-agent'
    start_urls = ['https://free-proxy-list.net/']
    start_urls = ['http://www.useragentstring.com/pages/useragentstring.php']
    start_urls = ['https://developers.whatismybrowser.com/useragents/explore/']

    def parse(self, response):
        print("Existing settings: %s" % self.settings.attributes.keys())