import os
import scrapy
from time import sleep
from scrapy.loader import ItemLoader
from scrapy.selector import Selector
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from scrapy_selenium import SeleniumRequest

basedir = os.path.dirname(os.path.realpath('__file__'))

class Hadist9SeleniumSpider(scrapy.Spider):

    # GET with JS
    # https://hadits.in/malik/1
    # better by ini karena ada definisi matan

    # POST API
    # https://hadits.in/viewer/service_eh2.php
    # form-data : {"jsonrpc":"2.0","method":"getHadits","params":["malik","1"],"id":1}
    # from-data : {"jsonrpc":"2.0","method":"getHadits","params":["malik","1594"],"id":1}
    
    name = "hadist9-seleniummiddleware"
    allowed_domains = ["hadits.in"]
    # start_urls = ['https://hadits.in/malik/1']
    start_urls = ['https://hadits.in/bukhari/1']
    

    custom_settings = {
        'ITEM_PIPELINES' : {
            # 'scrapme.pipelines.SQLiteDuplicatesPipeline.SQLiteDuplicatesPipeline': 100,
            # 'scrapme.pipelines.SQLiteSaveQuotesPipeline.SQLiteSaveQuotesPipeline': 200,
            'scrapme.pipelines.JsonLinesExporterPipeline.JsonLinesExporterPipeline': 300,
            # 'scrapme.pipelines.CsvExporterPipeline.CsvExporterPipeline': 400,
            # 'scrapme.pipelines.XmlExporterPipeline.XmlExporterPipeline': 500,
            # 'scrapme.pipelines.PickleExporterPipeline.PickleExporterPipeline': 600,
            # 'scrapme.pipelines.MarshalExporterPipeline.MarshalExporterPipeline': 700,
        },

        'SELENIUM_DRIVER_NAME': 'chrome',
        'SELENIUM_DRIVER_EXECUTABLE_PATH' : './chromedriver',
        'SELENIUM_DRIVER_ARGUMENTS' : [
            '--window-size=1920x1080',
            '--disk-cache-size=4096',
            # '--headless',
            'profile.managed_default_content_settings.images=2',
            ],

        #----------------
        # POLITE SPIDER
        #----------------

        'HTTPCACHE_ENABLED': True, # developement only
        # 'ROBOTSTXT_OBEY' : True,
        'RANDOMIZE_DOWNLOAD_DELAY' : True,
        # 'DOWNLOAD_DELAY' : 5,
        'DOWNLOADER_MIDDLEWARES' : {
            'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
            'scrapy_useragents.downloadermiddlewares.useragents.UserAgentsMiddleware': 500,
            # 'rotating_proxies.middlewares.RotatingProxyMiddleware': 610,
            # 'rotating_proxies.middlewares.BanDetectionMiddleware': 620,
            'scrapy_selenium.SeleniumMiddleware': 800
        },
        # 'USER_AGENT' : 'MyCompany-MyCrawler (bot@mycompany.com)',
        # https://developers.whatismybrowser.com/useragents/explore/
        'USER_AGENTS' : [ # rotate user agent
            ('Mozilla/5.0 (X11; Linux x86_64) '
            'AppleWebKit/537.36 (KHTML, like Gecko) '
            'Chrome/57.0.2987.110 '
            'Safari/537.36'),  # chrome
            ('Mozilla/5.0 (X11; Linux x86_64) '
            'AppleWebKit/537.36 (KHTML, like Gecko) '
            'Chrome/61.0.3163.79 '
            'Safari/537.36'),  # chrome
            ('Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:55.0) '
            'Gecko/20100101 '
            'Firefox/55.0')  # firefox
        ],
        'COOKIES_ENABLED' : False,
        'CONCURRENT_REQUESTS_PER_IP' : 10,
        # https://free-proxy-list.net
        # python get_proxy.py
        'ROTATING_PROXY_LIST_PATH' : 'get_proxy.txt',
        'DEFAULT_REQUEST_HEADERS' : {
            'Accept': 'application/json,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4',
            'Referer': 'https://hadits.in/malik/1' 
        },
        # 'AUTOTHROTTLE_ENABLED' : True,
        # 'AUTOTHROTTLE_DEBUG' : True,

    }

    def start_requests(self):
        yield SeleniumRequest(url=self.start_urls[0])

    def parse(self, response):

        print(response.request.meta['driver'].title)
        print(response.css('.menu-wrap').get())

        # chrome_options = Options()
        # chrome_options.add_argument("--window-size=1920x1080")
        # chrome_options.add_argument("--disk-cache-size=4096")
        # # chrome_options.add_argument("--headless")

        # prefs = {
        #     "profile.managed_default_content_settings.images": 2
        #     # 'disk-cache-size': 4096
        #     }
        # chrome_options.add_experimental_option('prefs', prefs)

        # chrome_driver_path = os.path.join(basedir, 'chromedriver')
        # driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=chrome_driver_path)
        
        # driver.get(self.start_urls[0])

        # scrapy_selector = Selector(text = driver.page_source)
        # content = scrapy_selector.css('.menu-wrap').get()
        
        # print(content)

        # driver.quit()



