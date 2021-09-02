from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from datetime import date
import scrapy
import time
import random

class LazadaSearchSpider(scrapy.Spider):
    name = "lazada"
    allowed_domains = ['lazada.co.id']
    
    custom_settings = {
        'HTTPCACHE_ENABLED': True,
        'ROBOTSTXT_OBEY' : False,
        #'FEED_URI' : 'lazadasearch.json',
        'DOWNLOADER_MIDDLEWARES' : {
            'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
            'scrapy_useragents.downloadermiddlewares.useragents.UserAgentsMiddleware': 500,
            'rotating_proxies.middlewares.RotatingProxyMiddleware': 610,
            'rotating_proxies.middlewares.BanDetectionMiddleware': 620,
            'scrapy_selenium.SeleniumMiddleware': 800
            }
        
        }
    def start_requests(self):
        url = 'https://www.lazada.co.id/catalog/?spm=a2o4j.home.search.1.11a715593k6cKb&q=rtx%203090&_keyori=ss&from=search_history&sugg=rtx%203090_0_1'
        yield scrapy.Request(url=url, callback=self.parse)
        
    def parse(self, response):
        options = webdriver.ChromeOptions()
        #options.add_experimental_option("detach", True)
        #options.add_argument("headless")
        #desired_capabilities = options.to_capabilities()
        driver = webdriver.Chrome(
            executable_path="./chromedriver.exe", 
            #desired_capabilities=desired_capabilities)
            chrome_options=options)
        
        driver.get('https://www.lazada.co.id')
        time.sleep(3)
        input_field = driver.find_element_by_xpath('//*[@id="q"]')
        input_field.send_keys('RTX 3090')
        input_field.send_keys(Keys.ENTER);
        time.sleep(3)
        
        try:
            last_page = driver.find_element_by_xpath('//*[@id="root"]/div/div[2]/div[1]/div/div[1]/div[3]/div/ul/li[8]').text
        except NoSuchElementException:
            last_page = '1'
        #last_page = 2
        link = []
        for page in range(int(last_page)):
        #for page in range(last_page):   
            last_height = driver.execute_script("return document.documentElement.scrollHeight")  
            while True:
                driver.execute_script("window.scrollBy(0, 900);")
                time.sleep(5)
                new_height = driver.execute_script("return document.documentElement.scrollHeight")
                if new_height == last_height:
                    break
                last_height = new_height
            
            
            #untuk dapetin tiap link (href)
            items_title = driver.find_elements_by_class_name('GridItem__title___8JShU')
            for item in items_title:
                item_href = item.find_element_by_xpath('./a').get_attribute('href')
                link.append(item_href)
            
            #click page selanjutnya
            next_button_container = driver.find_element_by_class_name('ant-pagination-next')
            next_button = next_button_container.find_element_by_css_selector('.ant-pagination-item-link')
            next_button.click()
            time.sleep(random.randint(5,7))
        
        #ambil item dari tiap link yang disimpen dalam list
        for l in link:
            driver.get(l)
            time.sleep(3)
            
            last_height = driver.execute_script("return document.documentElement.scrollHeight")  
            while True:
                driver.execute_script("window.scrollBy(0, 650);")
                time.sleep(random.randint(5, 10))
    
                new_height = driver.execute_script("return document.documentElement.scrollHeight")
                if new_height == last_height:
                    break
                last_height = new_height
            
            page_container = driver.find_element_by_xpath('//*[@id="container"]')
            
            #click view more di section spesifikasi
            try:
                view_more_button = page_container.find_element_by_css_selector('.pdp-view-more-btn.pdp-button.pdp-button_type_text.pdp-button_theme_white.pdp-button_size_m')
                driver.execute_script("arguments[0].scrollIntoView();", page_container.find_element_by_xpath('//*[@id="module_product_detail"]/div/div/div[1]'))
                time.sleep(random.randint(3,6))
                driver.execute_script("arguments[0].click();", view_more_button)
            except NoSuchElementException:
                pass
            
            item_title = page_container.find_element_by_xpath('//*[@id="module_product_title_1"]/div/div/h1').text
            item_seller = page_container.find_element_by_xpath('//*[@id="module_seller_info"]/div/div[1]/div[1]/div[2]/a').text
            item_price = page_container.find_element_by_xpath('//*[@id="module_product_price_1"]/div/div/span').text
            
            try:
                item_desc = page_container.find_element_by_css_selector('.html-content.pdp-product-highlights').text
            except NoSuchElementException:
                item_desc = ''
            try:
                item_rate = page_container.find_element_by_xpath('//*[@id="module_product_review"]/div/div/div[1]/div[2]/div/div/div[1]/div[1]/span[1]').text
            except NoSuchElementException: 
                item_rate = 0
            try:
                item_review = page_container.find_element_by_xpath('//*[@id="module_product_review"]/div/div/div[1]/div[2]/div/div/div[1]/div[3]').text
            except NoSuchElementException: 
                item_review = ''
            try:
                star_5 = page_container.find_element_by_xpath('//*[@id="module_product_review"]/div/div/div[1]/div[2]/div/div/div[2]/ul/li[1]/span[2]').text
                star_4 = page_container.find_element_by_xpath('//*[@id="module_product_review"]/div/div/div[1]/div[2]/div/div/div[2]/ul/li[2]/span[2]').text
                star_3 = page_container.find_element_by_xpath('//*[@id="module_product_review"]/div/div/div[1]/div[2]/div/div/div[2]/ul/li[3]/span[2]').text
                star_2 = page_container.find_element_by_xpath('//*[@id="module_product_review"]/div/div/div[1]/div[2]/div/div/div[2]/ul/li[4]/span[2]').text
                star_1 = page_container.find_element_by_xpath('//*[@id="module_product_review"]/div/div/div[1]/div[2]/div/div/div[2]/ul/li[5]/span[2]').text
            except NoSuchElementException:
                star_5 = ''
                star_4 = ''
                star_3 = ''
                star_2 = ''
                star_1 = ''
            
            arr_item_spec_key = []
            arr_item_spec_value = []
            try:
                item_specs = page_container.find_elements_by_class_name('key-li')
                for item in item_specs:
                    item_spec_key = item.find_element_by_xpath('./span').text
                    arr_item_spec_key.append(item_spec_key)
                    item_spec_value = item.find_element_by_xpath('./div').text
                    arr_item_spec_value.append(item_spec_value)
            except NoSuchElementException:
                arr_item_spec_key = []
                arr_item_spec_value = []
            yield{
                'url' : l,
                'item_title': item_title,
                'item_seller': item_seller,
                'item_price': item_price,
                'item_desc': item_desc,
                'item_spec_key': arr_item_spec_key, 
                'item_spec_value': arr_item_spec_value,
                'item_rate': item_rate,
                'item_review_count': item_review.replace(' Ratings', ''),
                'item_stars': {'5_stars': star_5,'4_stars': star_4,'3_stars': star_3,'2_stars' : star_2,'1_stars' : star_1}
                }