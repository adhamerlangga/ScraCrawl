from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from datetime import date
import scrapy
import time


class LinkedinProfileSpider(scrapy.Spider):
    name = "linkedin_profile"
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
        url = 'https://www.linkedin.com/school/telkom-university/posts/?feedView=all'
        yield scrapy.Request(url=url, callback=self.parse)
        
    def parse(self, response):
        options = webdriver.ChromeOptions()
        options.add_experimental_option("detach", True)
        #options.add_argument("headless")
        #desired_capabilities = options.to_capabilities()
        driver = webdriver.Chrome(
            executable_path="./chromedriver.exe", 
            #desired_capabilities=desired_capabilities)
            chrome_options=options)
        
        #untuk Login
        driver.get('https://www.linkedin.com/')
        
        try:
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
        
        except NoSuchElementException:
            sign_in_button = driver.find_element_by_xpath('/html/body/div[1]/main/p[1]/a')
            sign_in_button.click()
            
            #input username
            username = driver.find_element_by_name("session_key")
            username.send_keys('adhamsiwi@student.telkomuniversity.ac.id')
            time.sleep(1)
            
            #input password
            password = driver.find_element_by_name("session_password")
            password.send_keys('Zack Fair')
            time.sleep(1)
            
            button = driver.find_element_by_xpath('//*[@id="organic-div"]/form/div[3]/button')
            button.click()
            
        #pergi ke postnya telkom university
        driver.get("https://www.linkedin.com/school/telkom-university/posts/?feedView=all")
        time.sleep(10)
        
        last_height = driver.execute_script("return document.documentElement.scrollHeight")  
        while True:
            
            #scroll ke paling bawah page slider
            driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
    
            time.sleep(5)
            
            #itung height
            new_height = driver.execute_script("return document.documentElement.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
            
        all_post = driver.find_elements_by_css_selector('.occludable-update.ember-view')
        for post in all_post:
            driver.execute_script("arguments[0].scrollIntoView();", post)
            time.sleep(4)
            
            try:
                post_time_wrapper = post.find_element_by_css_selector(".feed-shared-actor__sub-description.t-12.t-normal.t-black--light")
                post_time = post_time_wrapper.find_element_by_class_name("visually-hidden").text
            except NoSuchElementException:
                post_time = '0'
            
            try:
                post_desc = post.find_element_by_class_name('break-words').text
            except NoSuchElementException:
                post_desc = ''
            
            try:
                post_react = post.find_element_by_css_selector('.v-align-middle.social-details-social-counts__reactions-count').text
            except NoSuchElementException:
                post_react = ''
                
            try:
                post_comment_count = post.find_element_by_css_selector('.social-details-social-counts__comments.social-details-social-counts__item').text
            except NoSuchElementException:
                post_comment_count = '0 comment'
            
            comment_username = []
            comment_time = []
            comment_job_title = []
            comment_text = []
            
            #apabila bukan post(iklan)
            try:
                social_button = post.find_element_by_css_selector('.feed-shared-social-actions.feed-shared-social-action-bar.social-detail-base-social-actions.feed-shared-social-action-bar--has-social-counts')
                comment_button = social_button.find_element_by_css_selector('.artdeco-button.artdeco-button--muted.artdeco-button--4.artdeco-button--tertiary.ember-view.comment-button.flex-wrap')
                driver.execute_script("arguments[0].scrollIntoView();", comment_button)
                driver.execute_script("arguments[0].click();", comment_button)
                time.sleep(5)
            except NoSuchElementException:
                pass
            
            #apabila ada komentar
            try:    
                comment_section = post.find_element_by_class_name('comments-comments-list')
                split = comment_section.text.split('\n')
                if "Load more comments" in split:
                    load_more_button = comment_section.find_element_by_css_selector('.comments-comments-list__load-more-comments-button.artdeco-button.artdeco-button--muted.artdeco-button--1.artdeco-button--tertiary.ember-view')
                    driver.execute_script("arguments[0].scrollIntoView();", load_more_button)
                    driver.execute_script("arguments[0].click();", load_more_button)
                    time.sleep(7)
                all_comments = comment_section.find_elements_by_css_selector('.comments-comment-item.comments-comments-list__comment-item')
                
                for c in all_comments:
                    comment_username.append(c.find_element_by_css_selector('.comments-post-meta__name-text.hoverable-link-text.mr1').text)
                    comment_time.append(c.find_element_by_css_selector('.comments-comment-item__timestamp.t-12.t-black--light.t-normal.mr1').text)
                    comment_job_title.append(c.find_element_by_css_selector('.comments-post-meta__headline.t-12.t-normal.t-black--light').text)
                    comment_text.append(c.find_element_by_css_selector('.feed-shared-text.relative').text)
                
            
            except NoSuchElementException: 
                comment_username = ''
                comment_time = ''
                comment_job_title = ''
                comment_text = ''
                
            yield {
                #"test": split,
                "post_time": post_time,
                "post_desc": post_desc,
                "post_react": post_react,
                "comment_count": post_comment_count,
                "comments": {
                    "comment_username": comment_username,
                    "comment_time": comment_time,
                    "comment_job_title": comment_job_title,
                    "comment_text": comment_text
                    }
            }
            #yang diambil: post_description, post_media, post_url, post_reaction, post_comment
        driver.close()

              