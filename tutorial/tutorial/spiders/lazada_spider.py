import scrapy
from tutorial.items import LazadaItem
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

class LazadaSpider(CrawlSpider):
    name = "LazadaItems"
    allowed_domains = ["lazada.sg"]
    start_urls = ['https://www.lazada.sg',
                  'https://www.lazada.sg/shop-audio/',
                  ]

    rules = (
        Rule(LinkExtractor(allow=('./products/.', )), callback='parse_item', follow=True),
        )

##    def start_requests(self):
##        urls = [
##            'https://www.lazada.sg/products/babyliss-pro-230-ceramic-hair-straightener-2069u-i153098018-s191124303.html?search=1&scm=1003.4.icms-zebra-5000374-2606919.ITEM_153098018_2280662'
##        ]
##        for url in urls:
##            yield scrapy.Request(url=url, callback=self.parse)

    def parse_item(self, response):
        self.logger.info('Hi, this is an item page! %s', response.url)
        item = LazadaItem()
        item['name'] = response.xpath('//*[@id="module_product_title_1"]/h1/text()').extract_first(default='null'),
        item['brand'] = response.xpath('//*[@id="module_product_brand_1"]/div/a[1]/text()').extract_first(default='null'),
        item['generalCat'] = response.xpath('//*[@id="J_breadcrumb"]/li[4]/span/a/span/text()').extract_first(default='null'),
        item['salePrice'] = response.xpath('//*[@id="module_product_price_1"]/div/span/text()').extract_first(default='null'),
        item['originalPrice'] = response.xpath('//*[@id="module_product_price_1"]/div/div/span[1]/text()').extract_first(default='null'),
        item['rating'] = response.xpath('//*[@id="module_product_review"]/div/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/span/text()').extract_first(default='null'),
        item['noOfRatings'] = response.xpath('//*[@id="module_product_review_star_1"]/div/a[1]/text()').extract_first(default='null'),
        item['positiveSellerRatings'] = response.xpath('//*[@id="module_seller_info"]/div/div[2]/div[1]/div/div/text()').extract_first(default='null'),
        item['returnPolicy'] = response.xpath('//*[@id="module_seller_warranty"]/div/div[2]/div[1]/div/div/div/div/text()').extract_first(default='null'),
        item['warranty'] = response.xpath('//*[@id="module_seller_warranty"]/div/div[2]/div[2]/div/div/div/div/text()').extract_first(default='null'),
        item['economyDeliveryPrice'] = response.xpath('//*[@id="module_seller_delivery"]/div/div/div[3]/div/div[2]/div/div/div[2]/text()').extract_first(default='null'),
        item['standardDeliveryPrice'] = response.xpath('//*[@id="module_seller_delivery"]/div/div/div[3]/div/div[3]/div/div/div[2]/text()').extract_first(default='null'),
        item['expressDeliveryPrice'] = response.xpath('//*[@id="module_seller_delivery"]/div/div/div[3]/div/div[4]/div/div/div[2]/text()').extract_first(default='null'),
        return item
            






                



        
##        items = LazadaItem()
##
##        yield {
##            'name' : response.xpath('//*[@id="module_product_title_1"]/h1/text()').extract_first(default='null'),
##            'brand' : response.xpath('//*[@id="module_product_brand_1"]/div/a[1]/text()').extract_first(default='null'),
##            'generalCat' : response.xpath('//*[@id="J_breadcrumb"]/li[4]/span/a/span/text()').extract_first(default='null'),
##            'salePrice' : response.xpath('//*[@id="module_product_price_1"]/div/span/text()').extract_first(default='null'),
##            'originalPrice' : response.xpath('//*[@id="module_product_price_1"]/div/div/span[1]/text()').extract_first(default='null'),
##            'rating' : response.xpath('//*[@id="module_product_review"]/div/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/span/text()').extract_first(default='null'),
##            'noOfRatings' : response.xpath('//*[@id="module_product_review_star_1"]/div/a[1]/text()').extract_first(default='null'),
##            'positiveSellerRatings' : response.xpath('//*[@id="module_seller_info"]/div/div[2]/div[1]/div/div/text()').extract_first(default='null'),
##            'returnPolicy' : response.xpath('//*[@id="module_seller_warranty"]/div/div[2]/div[1]/div/div/div/div/text()').extract_first(default='null'),
##            'warranty' : response.xpath('//*[@id="module_seller_warranty"]/div/div[2]/div[2]/div/div/div/div/text()').extract_first(default='null'),
##            'economyDeliveryPrice' : response.xpath('//*[@id="module_seller_delivery"]/div/div/div[3]/div/div[2]/div/div/div[2]/text()').extract_first(default='null'),
##            'standardDeliveryPrice' : response.xpath('//*[@id="module_seller_delivery"]/div/div/div[3]/div/div[3]/div/div/div[2]/text()').extract_first(default='null'),
##            'expressDeliveryPrice' : response.xpath('//*[@id="module_seller_delivery"]/div/div/div[3]/div/div[4]/div/div/div[2]/text()').extract_first(default='null'),
##}            



        
##        next_page = response.css('li.next a::attr(href)').extract_first()
##        if next_page is not None:
##            next_page = response.urljoin(next_page)
##            yield scrapy.Request(next_page, callback=self.parse)
##
##            
##        page = response.url.split("/")[-2]
##        filename = 'quotes-%s.html' % page
##        with open(filename, 'wb') as f:
##            f.write(response.body)
##        self.log('Saved file %s' % filename)
