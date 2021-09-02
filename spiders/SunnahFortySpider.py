import scrapy


class SunnahFortySpider(scrapy.Spider):
    name = "Forty"
    allowed_domains = ['sunnah.com']
    start_urls = ['https://sunnah.com/forty']
    base_url = 'https://sunnah.com/forty'

    def parse(self, response):
        books = response.css('div.book_title.title')
        
        for book in books:
            
            #go to book page
            book_url = book.xpath('./a').attrib['href']
            yield response.follow(book_url, callback = self.parse_hadits)
            
    def parse_hadits(self, response):
        hadits_container = response.css('div.actualHadithContainer.hadith_container_forty')
        hadits = []
        for h in hadits_container:
            first_text_container = h.css('div.hadith_narrated')
            hadits.append({
                'first_text':first_text_container.css('p::text').get(),
                'second_text': h.css('div.text_details::text').get(),
                'arabic' : h.xpath('./div[@class="arabic_hadith_full arabic"]/descendant::*/text()').get(),
                'grade' : h.css('td.english_grade::text').get(),
                'reference': h.xpath('./div[@class="bottomItems"]/table//td/a/text()').get()
        })
        yield{
            'book_number': response.css('div.book_page_number::text').get(),
            'book_name_en': response.css('div.book_page_english_name::text').get().split('\t')[4],
            'book_name_ar': response.css('div.book_page_arabic_name.arabic::text').get(),
            'content': hadits,
            }