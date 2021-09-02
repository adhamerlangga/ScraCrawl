from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from datetime import date
import undetected_chromedriver as uc
import scrapy
import time
import random


class IbnuSpider(scrapy.Spider):
    name = "ibnumajah"
    allowed_domains = ['hadits.in']
    
    custom_settings = {
        'HTTPCACHE_ENABLED': True,
        'ROBOTSTXT_OBEY' : False,
        #'FEED_URI' : 'linkedin.json',
        'DOWNLOADER_MIDDLEWARES' : {
            'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
            'scrapy_useragents.downloadermiddlewares.useragents.UserAgentsMiddleware': 500,
            'rotating_proxies.middlewares.RotatingProxyMiddleware': 610,
            'rotating_proxies.middlewares.BanDetectionMiddleware': 620,
            'scrapy_selenium.SeleniumMiddleware': 800
            },
        
        }
    def start_requests(self):
        url = 'https://www.google.com'
        yield scrapy.Request(url=url, callback=self.parse)
        
    def parse(self, response):
        options = webdriver.ChromeOptions() 
        driver = uc.Chrome(options=options)
        
        #halaman terakhir 4332
        driver.get("https://hadits.in/ibnumajah/1")
        wait = WebDriverWait(driver, 10)
        while True:
            
            container = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/div/div[1]/div/div[2]/div')))
            
            arab = container.find_element_by_class_name('ScheherazadeW').text
            bahasa = container.find_element_by_class_name('mykitab-secondary').text
            
            yield {
                'url': driver.current_url,
                'arab': arab,
                'bahasa': bahasa
            }
            
            next_page = driver.find_element_by_xpath('/html/body/div[3]/div/div[1]/div/div[10]/a').get_attribute('href')
            
            if next_page != 'https://hadits.in/ibnumajah/undefined':
                driver.get(next_page)
            else: 
                break
            
        driver.quit()
        
        