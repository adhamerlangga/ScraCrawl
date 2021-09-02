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

class Hadist9Spider(scrapy.Spider):

    # GET with JS
    # https://hadits.in/malik/1
    # better by ini karena ada definisi matan

    # POST API
    # https://hadits.in/viewer/service_eh2.php
    # form-data : {"jsonrpc":"2.0","method":"getHadits","params":["malik","1"],"id":1}
    # from-data : {"jsonrpc":"2.0","method":"getHadits","params":["malik","1594"],"id":1}
    
    name = "hadist9"
    allowed_domains = ["hadits.in"]
    start_urls = [
        'https://hadits.in/bukhari/1',
        ]
    
    def parse(self, response):

        chrome_options = Options()
        
        # Preferences
        # https://src.chromium.org/viewvc/chrome/trunk/src/chrome/common/pref_names.cc?view=markup
        # disable image download
        prefs = {"profile.managed_default_content_settings.images":2}
        chrome_options.add_experimental_option('prefs', prefs)

        # Arguments
        # https://peter.sh/experiments/chromium-command-line-switches/
        chrome_options.add_argument("--headless")
        # chrome_options.add_argument("--window-size=1920x1080")
        chrome_options.add_argument("--disk-cache-size=5242880")

        chrome_driver_path = os.path.join(basedir, 'chromedriver')
        driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=chrome_driver_path)
        
        driver.get(self.start_urls[0])
        scrapy_selector = Selector(text = driver.page_source)

        # print(scrapy_selector.css('.menu-wrap').get())
        print('ARAB : ' + scrapy_selector.css('.ScheherazadeW::text').get())
        print('INDONESIA : ' + scrapy_selector.css('.mykitab-secondary::text').get())
        
        driver.quit()



