import scrapy
import json
import requests as rq
from Hsn.items import HSNItem

count = 0
class HSNSpider(scrapy.Spider):
    name = "HSNItems"
    start_urls = [
                  'https://www.hsn.com/shop/computers/ec0027?view=all',
                  ]

    def parse(self, response):
##        result = response.css('script').extract()[2]
##        result = result.replace('</script>',"")
##        result = result.replace('<script>window.pageData=',"")
        links = response.xpath('//div[not(@*)]/a/@href').extract()
        for item in links:
##            href = "https://www.hsn.com/products" + item
            print("Link: ", item)
            yield response.follow(item, self.parse_review)
        next_page = response.xpath('//*[@id="template-product-grid"]/div[1]/div[2]/div[2]/div[2]/div/nav/ul/li[2]/a/@href').extract_first(default='null')
        if next_page != 'null':
            next_page = response.urljoin(next_page)
            print("Next page: ", next_page)
            yield scrapy.Request(next_page, callback=self.parse, dont_filter = True)

    


    def parse_item(self, response):
        global count
        next_review_page = response.xpath('//*[@id="product-detail-reviews"]/div[3]/div/nav/ul/li[1]/@href').extract_first(default='null')
        print("Next review: \n\n", next_review_page)
        data = {}
        for i in response.xpath('//tr[not(@*)]/td/text()').extract():
            if i.strip() != "":
                 data[i.strip()] = response.xpath('//tr[not(@*)]/td/span/text()').extract()[count]
                 count+=1
        count=0
        json_data = json.dumps(data)
        item = HSNItem()
##        item['name'] = response.xpath('//*[@id="product-name"]/text()').extract_first(default='null'),
##        item['price'] = response.xpath('//*[@id="template-product-detail-product"]/div[2]/div[2]/div[1]/div[1]/div/span[1]/text()').extract_first(default='null') + response.xpath('//*[@id="template-product-detail-product"]/div[2]/div[2]/div[1]/div[1]/div/span[2]/text()').extract_first(default='null'),
##        item['savings'] = response.xpath('//*[@id="template-product-detail-product"]/div[2]/div[2]/div[2]/div[2]/span/text()').extract_first(default='null'),
##        item['altPayment'] = response.xpath('//*[@id="template-product-detail-product"]/div[2]/div[2]/div[1]/div[2]/text()').extract_first().strip() + " * " + response.xpath('//*[@id="template-product-detail-product"]/div[2]/div[3]/form/div[3]/p/label/a/text()').extract()[0].strip(),
##        item['giftEligibility'] = response.xpath('//*[@id="template-product-detail-product"]/div[2]/div[3]/form/p[1]/span/@data-tooltip').extract_first(default='null'),
##        item['productDesc'] = json_data,
        item['noOfReviews'] = response.xpath('//*[@id="product-detail-reviews"]/div[1]/div[1]/div[2]/span/text()').extract_first(default='null').strip(),
##        item['rating'] = response.xpath('//*[@id="product-detail-reviews"]/div[1]/div[1]/div[2]/span/span/text()').extract_first(default='null').strip(),
        ##item['review'] = response.xpath('//div[@class="copy"]/p/text()').extract(),
##        item['review'] = ,
##        item['rating'] = ,
##        item['rating'] = ,
####            'noOfRatings' : response.xpath('//*[@id="module_product_review_star_1"]/div/a[1]/text()').extract_first(default='null'),
##            'colour' : response.xpath('//*[@id="productDetails"]/table/tr[2]/td[2]/text()').extract_first(default='null').strip(),
##            'careLabel' : response.xpath('//*[@id="productDetails"]/table/tr[3]/td[2]/text()').extract_first(default='null').strip(),
##            'material' : response.xpath('//*[@id="productDetails"]/table/tr[4]/td[2]/text()').extract_first(default='null').strip(),
##            'xSmall' : response.xpath('//*[@id="sizeDetails"]/div[1]/span/text()[2]').extract_first(default='null'),
##            'small' : response.xpath('///*[@id="sizeDetails"]/div[1]/span/text()[3]').extract_first(default='null'),
##            'medium' : response.xpath('//*[@id="sizeDetails"]/div[1]/span/text()[4]').extract_first(default='null'),
##            'large' : response.xpath('//*[@id="sizeDetails"]/div[1]/span/text()[5]').extract_first(default='null'),
##            'xLarge' : response.xpath('//*[@id="sizeDetails"]/div[1]/span/text()[6]').extract_first(default='null'),
##            'cashOnDelivery' : response.xpath('//*[@id="product-box"]/div/div[1]/section/div[1]/div[2]/div/ul/li[3]/span[2]/text()').extract_first(default='null'),
##            '30d_return' : response.xpath('//*[@id="cms-freeReturn"]/span[2]/text()').extract_first(default='null'),
##            'delivery_above_$40' : response.xpath('//*[@id="cms-usp__freeshipping"]/span[2]/text()').extract_first(default='null'),
##            'deliver_date' : response.xpath('//*[@id="estimated_delivery_time"]/text()').extract_first(default='null'),

        return item
    
    def parse_review(self, response):
      item = HSNItem()
      next_review_page = response.xpath('//*[@id="product-detail-reviews"]/div[3]/div/nav/ul/li[1]/@href').extract_first(default='null')
      if next_review_page != 'null':
          print(next_review_page)
#          print(rq.get(next_review_page).text)
          yield response.follow(next_review_page, callback=self.parse_item, dont_filter = True)
      return item
        

