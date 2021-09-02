from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import date
import scrapy
import time


class YoutubeProfileSpider(scrapy.Spider):
    name = "youtube"
    allowed_domains = ['youtube.com']
    
    custom_settings = {
        'HTTPCACHE_ENABLED': True,
        'ROBOTSTXT_OBEY' : False,
        #'FEED_URI' : 'youtube.json',
        'DOWNLOADER_MIDDLEWARES' : {
            'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
            'scrapy_useragents.downloadermiddlewares.useragents.UserAgentsMiddleware': 500,
            'rotating_proxies.middlewares.RotatingProxyMiddleware': 610,
            'rotating_proxies.middlewares.BanDetectionMiddleware': 620,
            'scrapy_selenium.SeleniumMiddleware': 800
            }
        
        }
    def start_requests(self):
        url = 'https://www.youtube.com/c/TelkomUniversityOfficial/videos?view=0&sort=p&flow=grid'
        yield scrapy.Request(url=url, callback=self.parse)
        
    def parse(self, response):
        options = webdriver.ChromeOptions()
        #options.add_experimental_option("detach", True)
        options.add_argument("headless")
        desired_capabilities = options.to_capabilities()
        driver = webdriver.Chrome(
            executable_path="./chromedriver.exe", 
            desired_capabilities=desired_capabilities)
            #chrome_options=options)
        driver.get("https://www.youtube.com/c/TelkomUniversityOfficial/videos?view=0&sort=p&flow=grid")
        time.sleep(5)
        
        last_height = driver.execute_script("return document.documentElement.scrollHeight")              
        while True:
        # Scroll down 'til "next load".
            driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")

        # Wait to load everything thus far.
            time.sleep(5)

        # Calculate new scroll height and compare with last scroll height.
            new_height = driver.execute_script("return document.documentElement.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
        
        videos = driver.find_elements_by_id('dismissible')
        arr_link = []
        for video in videos:
            video_link = video.find_element_by_css_selector('.yt-simple-endpoint.inline-block.style-scope.ytd-thumbnail').get_attribute('href')
            arr_link.append(video_link)
            
        for link in arr_link:
            time.sleep(10)
            driver.get(link)
            time.sleep(5)
            
            #extract video section
            video_id = link.strip('https://www.youtube.com/watch?v=')
            v = driver.find_element_by_xpath('//*[@id="content"]')
            title = v.find_element_by_xpath('//*[@id="container"]/h1/yt-formatted-string').text
            video_publish_date = v.find_element_by_xpath('//*[@id="info-strings"]/yt-formatted-string').text
            video_view_count = v.find_element_by_xpath('//*[@id="count"]/ytd-video-view-count-renderer/span[1]').text
            video_time = v.find_element_by_xpath('//*[@id="info-strings"]/yt-formatted-string').text
            video_like_count = driver.find_element_by_xpath('/html/body/ytd-app/div/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/div[8]/div[2]/ytd-video-primary-info-renderer/div/div/div[3]/div/ytd-menu-renderer/div/ytd-toggle-button-renderer[1]/a/yt-formatted-string').text
            video_dislike_count = driver.find_element_by_xpath('/html/body/ytd-app/div/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/div[8]/div[2]/ytd-video-primary-info-renderer/div/div/div[3]/div/ytd-menu-renderer/div/ytd-toggle-button-renderer[2]/a/yt-formatted-string').text
            video_channel = driver.find_element_by_xpath('/html/body/ytd-app/div/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/div[9]/div[2]/ytd-video-secondary-info-renderer/div/div/ytd-video-owner-renderer/div[1]/ytd-channel-name/div/div/yt-formatted-string/a').text
            video_url_channel = driver.find_element_by_xpath('/html/body/ytd-app/div/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/div[9]/div[2]/ytd-video-secondary-info-renderer/div/div/ytd-video-owner-renderer/div[1]/ytd-channel-name/div/div/yt-formatted-string/a').get_attribute('href')
            video_subscriber = driver.find_element_by_xpath('/html/body/ytd-app/div/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/div[9]/div[2]/ytd-video-secondary-info-renderer/div/div/ytd-video-owner-renderer/div[1]/yt-formatted-string').text
            video_description = str(driver.find_element_by_xpath('//*[@id="description"]/yt-formatted-string').text)#+ str(driver.find_element_by_xpath('//*[@id="description"]/yt-formatted-string/a').get_attribute('href'))
            comment_section = v.find_element_by_xpath('//*[@id="comments"]')
            
            # Scroll into view the comment section, then allow some time for everything to be loaded as necessary.
            driver.execute_script("arguments[0].scrollIntoView();", comment_section)
            time.sleep(5)
        
            last_height = driver.execute_script("return document.documentElement.scrollHeight")  
            while True:
            # Scroll down 'til "next load".
                driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
    
            # Wait to load everything thus far.
                time.sleep(5)
    
            # Calculate new scroll height and compare with last scroll height.
                new_height = driver.execute_script("return document.documentElement.scrollHeight")
                if new_height == last_height:
                    break
                last_height = new_height
             
            # One last scroll just in case.
            #driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
            
            #extract comment section
            comment_wrappers = v.find_elements_by_css_selector('#contents #comment')
            comment_username_elems = v.find_elements_by_xpath('//*[@id="author-text"]')
            comment_elems = v.find_elements_by_xpath('//*[@id="content-text"]')
            get_href_comment_userlink = v.find_elements_by_xpath('//*[@id="author-text"]')
            comment_like_counter_elems = v.find_elements_by_xpath('//*[@id="vote-count-middle"]')
            comment_time_elems = v.find_elements_by_xpath('//*[@id="header-author"]/yt-formatted-string/a')
            
            #ngambil jumlah comment
            #limiter = int(driver.find_element_by_xpath('//*[@id="count"]/yt-formatted-string/span[1]').text)
            
            #limiter = 100
            
            for comment_wrapper,comment_username, comment , comment_userlink,comment_like_counter, comment_time in zip\
                (comment_wrappers,comment_username_elems,comment_elems, get_href_comment_userlink,comment_like_counter_elems,
                  comment_time_elems):
                
                replies_section = comment_wrapper.find_element_by_xpath('..//*[@id="replies"]')
                if replies_section.text.startswith('View'):
                    reply = replies_section.find_element_by_css_selector('a')
                    driver.execute_script("arguments[0].scrollIntoView();", reply)
                    driver.execute_script('window.scrollTo(0,(window.pageYOffset-150))') # cater for the youtube header
                    driver.execute_script("arguments[0].click();", reply)
                    time.sleep(5)
                    
                    #kondisi untuk reply = 1
                    split = replies_section.text.split('\n')
                    if "Hide reply" in split:
                        reply_username = replies_section.find_element_by_id('author-text').text
                        reply_userlink = replies_section.find_element_by_id('author-text').get_attribute('href')
                        reply_comment = replies_section.find_element_by_id('content-text').text
                        reply_like = replies_section.find_element_by_id('vote-count-middle').text
                        reply_time = replies_section.find_element_by_class_name('published-time-text.above-comment.style-scope.ytd-comment-renderer').text
                            
                    #kondisi untuk reply selain dari 1    
                    else:
                        reply_username = []
                        reply_userlink = []
                        reply_comment = []
                        reply_like = []
                        reply_time = []
                        
                        for reply in replies_section.find_elements_by_id('author-text'):
                            reply_username.append(reply.text)
                            reply_userlink.append(reply.get_attribute('href'))
                            
                        for reply in replies_section.find_elements_by_id('content-text'):
                            reply_comment.append(reply.text)
                    
                        for reply in replies_section.find_elements_by_id('vote-count-middle'):
                            reply_like.append(reply.text)
                        
                        for reply in replies_section.find_elements_by_class_name('published-time-text.above-comment.style-scope.ytd-comment-renderer'):
                            reply_time.append(reply.text)
                
                else:
                    reply_username = '' 
                    reply_userlink = ''
                    reply_comment = ''
                    reply_like  = ''
                    reply_time = ''
                        
                yield {
                    #"test" : video.text,
                    #"split": split,
                    
                    "video_id": video_id,
                    "video_scrap_time" : date.today() ,
                    "video_publish_date": video_publish_date,
                    "video_title" : title,
                    "video_view_count": video_view_count,  
                    "video_time": video_time,
                    "video_like_count": video_like_count,
                    "video_dislike_count": video_dislike_count,
                    "video_channel": video_channel,
                    'video_url_channel' : video_url_channel,
                    "video_subscriber": video_subscriber,
                    "video_description": video_description,
                    
                    "comment_username": comment_username.text,
                    "comment_userlink ": comment_userlink.get_attribute("href"),
                    "comment": comment.text,
                    "comment_like_counter": comment_like_counter.text,
                    "comment_time" :comment_time.text,
                    "comment_reply": {'reply_username': reply_username,'reply_userlink':reply_userlink,'reply_comment':reply_comment,'reply_like':reply_like,'reply_time':reply_time},
                    
                    }
            driver.get("https://www.youtube.com/c/TelkomUniversityOfficial/videos?view=0&sort=p&flow=grid")
            
        driver.close()

              