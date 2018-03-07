import scrapy
import json

count = 1
class LazadaSpider(scrapy.Spider):
    name = "LazadaItems"
    start_urls = [
                  'https://www.lazada.sg/shop-audio/',
                  ]

    def parse(self, response):
        result = response.css('script').extract()[2]
        result = result.replace('</script>',"")
        result = result.replace('<script>window.pageData=',"")
        data = json.loads(result)
        for item in data["mods"]["listItems"]:
            href = item["productUrl"]
            yield response.follow(str(href), self.parse_item)
        global count
        count += 1
        next_page = 'https://www.lazada.sg/shop-audio/?page=' + str(count)
        if count < 103:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)


    def parse_item(self, response):
        yield {
            'name' : response.xpath('//*[@id="module_product_title_1"]/h1/text()').extract_first(default='null'),
            'brand' : response.xpath('//*[@id="module_product_brand_1"]/div/a[1]/text()').extract_first(default='null'),
            'generalCat' : response.xpath('//*[@id="J_breadcrumb"]/li[4]/span/a/span/text()').extract_first(default='null'),
            'salePrice' : response.xpath('//*[@id="module_product_price_1"]/div/span/text()').extract_first(default='null'),
            'originalPrice' : response.xpath('//*[@id="module_product_price_1"]/div/div/span[1]/text()').extract_first(default='null'),
            'rating' : response.xpath('//*[@id="module_product_review"]/div/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/span/text()').extract_first(default='null'),
            'noOfRatings' : response.xpath('//*[@id="module_product_review_star_1"]/div/a[1]/text()').extract_first(default='null'),
            'positiveSellerRatings' : response.xpath('//*[@id="module_seller_info"]/div/div[2]/div[1]/div/div/text()').extract_first(default='null'),
            'returnPolicy' : response.xpath('//*[@id="module_seller_warranty"]/div/div[2]/div[1]/div/div/div/div/text()').extract_first(default='null'),
            'warranty' : response.xpath('//*[@id="module_seller_warranty"]/div/div[2]/div[2]/div/div/div/div/text()').extract_first(default='null'),
            'economyDeliveryPrice' : response.xpath('//*[@id="module_seller_delivery"]/div/div/div[3]/div/div[2]/div/div/div[2]/text()').extract_first(default='null'),
            'standardDeliveryPrice' : response.xpath('//*[@id="module_seller_delivery"]/div/div/div[3]/div/div[3]/div/div/div[2]/text()').extract_first(default='null'),
            'expressDeliveryPrice' : response.xpath('//*[@id="module_seller_delivery"]/div/div/div[3]/div/div[4]/div/div/div[2]/text()').extract_first(default='null'),
        }


