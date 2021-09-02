import scrapy


class SunnahNawawiSpider(scrapy.Spider):
    name = "Nawawi"
    allowed_domains = ['sunnah.com']
    start_urls = ['https://sunnah.com/nawawi40']
    base_url = 'https://sunnah.com/nawawi40'
            
    def parse(self, response):
        hadits_container = response.css('div.actualHadithContainer.hadith_container_forty')
        #hadits = []
        auth_intro_eng = response.xpath('//*[@id="main"]/div[2]/div[3]/div[1]/p/text()').get()
        auth_intro_arb = response.xpath('//*[@id="main"]/div[2]/div[3]/div[2]/p/text()').get()
        
        for h in hadits_container:
            # hadits.append({
            #     'first_text':h.css('div.hadith_narrated::text').get(),
            #     'second_text': h.css('div.text_details::text').get(),
            #     'arabic' : h.css('div.arabic_hadith_full.arabic::text').get(),
            #     'grade' : h.css('td.english_grade::text').get(),
            # })
            
            first_text_container = h.css('div.hadith_narrated')
            first_text = first_text_container.css('p::text').get()
            second_text = h.css('div.text_details::text').get()
            arabic = h.css('div.arabic_hadith_full.arabic::text').get()
            ref = h.xpath('./div[@class="bottomItems"]/table//td/a/text()').get()
            
            yield{
                'auth_intro_eng': auth_intro_eng,
                'auth_intro_arb': auth_intro_arb,
                'first_text':first_text,
                'second_text':second_text,
                'arabic_text':arabic,
                'reference':ref,
                }