from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from datetime import date
import scrapy
import time


class LinkedinSpider(scrapy.Spider):
    name = "linkedin"
    allowed_domains = ['linkedin.com']
    
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
            }
        
        }
    def start_requests(self):
        url = 'https://www.linkedin.com/search/results/content/?keywords=telkom%20university&origin=GLOBAL_SEARCH_HEADER&update=urn%3Ali%3Afs_updateV2%3A(urn%3Ali%3Aactivity%3A6816226134208860160%2CBLENDED_SEARCH_FEED%2CEMPTY%2CDEFAULT%2Cfalse)'
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
        
        #untuk Login
        driver.get('https://www.linkedin.com/')
        
        #input username
        username = driver.find_element_by_name("session_key")
        username.send_keys('adhamsiwi@student.telkomuniversity.ac.id')
        time.sleep(1)
        
        #input password
        password = driver.find_element_by_name("session_password")
        password.send_keys('Zack Fair')
        time.sleep(1)
        
        #click sign in button
        sign_in_button = driver.find_element_by_class_name('sign-in-form__submit-button')
        sign_in_button.click()
        time.sleep(2)
        
        #buka hasil search Telkom University
        
        # driver.get('https://www.linkedin.com/feed/')
        # search_button = driver.find_element_by_xpath('//*[@id="ember19"]/input')
        # search_button.click()
        # time.sleep(3)
        # search_button.send_keys("Telkom University")
        # search_button.send_keys(Keys.ENTER)
        # time.sleep(15)
        
        # post_button = driver.find_element_by_css_selector('.artdeco-pill.artdeco-pill--slate.artdeco-pill--2.artdeco-pill--choice.ember-view.search-reusables__filter-pill-button')
        # post_button.click()
        driver.get("https://www.linkedin.com/search/results/content/?keywords=telkom%20university&origin=GLOBAL_SEARCH_HEADER&sid=2Qo")
        time.sleep(10)
        
        #limiter = 0
        page = 2
        while page <= 43:
            #container yang bungkus kanan kiri
            main_container= driver.find_element_by_xpath('//*[@id="main"]/div')
        
            #execute javascript untuk click tiap postingan
            card_container_elems = main_container.find_elements_by_css_selector(".reusable-search__result-container.artdeco-card.search-results__hide-divider.mb3")
            #i = len(card_container_elems)
            for card_container in card_container_elems:
                driver.execute_script("arguments[0].scrollIntoView();", card_container)
                card_container.click()
                time.sleep(5)
                                
                post_username = main_container.find_element_by_css_selector('.feed-shared-actor__name.t-14.t-bold.hoverable-link-text.t-black').text
                try:
                    post_job_title = main_container.find_element_by_css_selector('.feed-shared-actor__description.t-12.t-normal.t-black--light').text
                except NoSuchElementException:
                    post_job_title = ''
                time_container = main_container.find_element_by_css_selector('.feed-shared-actor__sub-description.t-12.t-normal.t-black--light')
                post_time = time_container.find_element_by_class_name('visually-hidden').text
                try:
                    post_description = main_container.find_element_by_class_name('break-words').text
                except NoSuchElementException:
                    post_description = ''
                try:
                    #if medianya picture 
                    post_picture = main_container.find_element_by_class_name('feed-shared-image__container').get_attribute('src')
                except NoSuchElementException:
                    post_picture = ''
                    
                try: 
                    #if medianya video
                    post_video = main_container.find_element_by_class_name('feed-shared-linkedin-video__container').get_attribute('src')
                except NoSuchElementException:
                    post_video = ''
                try:
                    #if medianya slide
                    post_slide = main_container.find_element_by_css_selector('.carousel-lazy-element.carousel-element-loaded.carousel-element-load-success').get_attribute('data-src')  
                except NoSuchElementException:
                    post_slide = ''
                
                try:
                    #if medianya artikel
                    post_article = main_container.find_element_by_class_name('feed-shared-article__link-container').get_attribute('src')  
                except NoSuchElementException:
                    post_article = ''
                    
                try:
                    #if medianya dokumen
                    post_document = main_container.find_element_by_class_name('document-s-container').get_attribute('data-src')  
                except NoSuchElementException:
                    post_document = ''
                    
                comment_username = []
                comment_job_title = []
                comment_time = []
                
                
                try:
                    post_reaction = main_container.find_element_by_css_selector('.v-align-middle.social-details-social-counts__reactions-count').text
                except NoSuchElementException:
                    post_reaction = ''
                    
                try:
                    post_comment = main_container.find_element_by_class_name('v-align-middle').text
                    comments = main_container.find_elements_by_class_name('comments-comment-item')
                    
                    for comment in comments:
                        comment_username.append(comment.find_element_by_css_selector('.comments-post-meta__name-text.hoverable-link-text.mr1').text)
                        comment_job_title.append(comment.find_element_by_css_selector('.comments-post-meta__headline.t-12.t-normal.t-black--light').text)
                        comment_time.append(comment.find_element_by_css_selector('.comments-comment-item__timestamp.t-12.t-black--light.t-normal.mr1').text)
                        
                except NoSuchElementException:
                    post_comment = ''
                    
                
                yield {
                    
                    'post_username': post_username,
                    'post_job_title': post_job_title,
                    'post_description': post_description,
                    'post_time': post_time,
                    'post_reaction': post_reaction,
                    'post_comment': post_comment,
                    'post_picture': post_picture,
                    'post_video': post_video,
                    'post_slide': post_slide,
                    'post_article': post_article,
                    'post_document': post_document,
                    
                    'comment_username': comment_username,
                    'comment_job_title': comment_job_title,
                    'comment_time': comment_time,
                    
                    
                    }
            #limiter = limiter + i
            
            #disini click page selanjutnya
            time.sleep(30)
            page_click = driver.find_element_by_xpath(f"//button[@aria-label='Page {page}']")
            driver.execute_script("arguments[0].click();", page_click)
            time.sleep(30)
                
            page += 1
            # if limiter >= 100:
            #     break
        
        driver.close()

              