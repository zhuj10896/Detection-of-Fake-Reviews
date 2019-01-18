import scrapy

# genspider
class HotelTpSpider(scrapy.Spider):
    name = 'Hotel_WAD'
    allowed_domains = ['www.tripadvisor.com']
    start_urls = [
                  'https://www.tripadvisor.com/Hotel_Review-g60898-d1199584-Reviews-W_Atlanta_Downtown-Atlanta_Georgia.html/']
                  
    #function 
    def parse(self,response):
        #commet big blocks in each page and have 5 big blocks.
        hotelb = response.xpath('//*[@class="reviewSelector"]') #div
        #varibles in this loop running different big block.
        for hotel in hotelb:
            hotel_name = response.xpath('//*[@id="HEADING"]/text()').extract_first()
            hotel_address = response.xpath('//*[@id="taplc_resp_hr_atf_hotel_info_0"]/div/div[2]/div/div[2]/div/div[1]/span[2]/span[1]/text()').extract()
            review_date = hotel.xpath('.//*[@class="ratingDate"]/text()').extract_first()
            username = hotel.xpath('.//*[@class="info_text"]/div/text()').extract_first()
            number_reviewsandlikes = hotel.xpath('.//*[@class="badgetext"]/text()').extract()
            #number_contributions = hotel.xpath('.//*[@class="copy_number"]/text()').extract()
            headers = hotel.xpath('.//*[@class="noQuotes"]/text()').extract()
            #content = hotel.xpath('.//*[@class="partial_entry"]/text()').extract_first()
            yield {'Hotel name': hotel_name,'Hotel Address': hotel_address,'Review Date': review_date,'Username': username,'Number of reviews and likes': number_reviewsandlikes,'Headers': headers}
        #move on to next pages 
        next_page_url = response.xpath('//*[@class="nav next taLnk ui_button primary"]/@href').extract_first()
        absolute_next_page_url = response.urljoin(next_page_url)
        yield scrapy.Request(absolute_next_page_url)