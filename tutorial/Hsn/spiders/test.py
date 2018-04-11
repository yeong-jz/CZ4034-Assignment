import scrapy
import json
import requests as rq
from Hsn.items import HSNItem

count = 0
class HSNSpider(scrapy.Spider):
    name = "HSNItems"
    start_urls = [
                  'https://www.hsn.com/shop/computers/ec0027?view=all',
                  'https://www.hsn.com/shop/audio/ec0202?view=all',
                  'https://www.hsn.com/shop/cameras-photo-and-video/ec0405?view=all',
                  'https://www.hsn.com/shop/car-electronics/ec0427?view=all',
                  'https://www.hsn.com/shop/headphones/ec0442?view=all',
                  'https://www.hsn.com/shop/home-office/ec0573?view=all',
                  'https://www.hsn.com/shop/portable-chargers-and-batteries/ec0484?view=all',
                  'https://www.hsn.com/shop/printers/ec0454?view=all',
                  'https://www.hsn.com/shop/shredders/ec0455?view=all',
                  'https://www.hsn.com/shop/smart-home/ec0447?view=all',
                  'https://www.hsn.com/shop/software/ec0304?view=all',
                  'https://www.hsn.com/shop/tablets/ec0476?view=all',
                  'https://www.hsn.com/shop/video-games-and-systems/ec0220?view=all',
                  'https://www.hsn.com/shop/tvs-and-home-theater/ec0073?view=all',
                  'https://www.hsn.com/shop/wearable-tech/ec0544?view=all',
                  'https://www.hsn.com/shop/televisions/ec0137?view=all',
                  'https://www.hsn.com/shop/cell-phones/ec0373?view=all',
                  'https://www.hsn.com/shop/womens-clothing/fa0153?view=all',
                  'https://www.hsn.com/shop/shoes/fa0045?view=all',
                  'https://www.hsn.com/shop/socks/fa0142?view=all',
                  'https://www.hsn.com/shop/wide-width-shoes/fa0045-7106?view=all',
                  'https://www.hsn.com/shop/kids-shoes/fa0143?view=all',
                  'https://www.hsn.com/shop/beauty/bs?view=all',
                  'https://www.hsn.com/shop/jewelry/j?view=all',
                  'https://www.hsn.com/shop/kitchen-and-food/qc?view=all',
                  'https://www.hsn.com/shop/appliances/qc0010?view=all',
                  'https://www.hsn.com/shop/cookware/qc0001?view=all',
                  'https://www.hsn.com/shop/food-and-beverages/qc0037?view=all',
                  'https://www.hsn.com/shop/health-and-fitness/hf?view=all',
                  'https://www.hsn.com/shop/crafts-and-sewing/ct?view=all',
                  'https://www.hsn.com/shop/travel/9365?view=all',
                  'https://www.hsn.com/shop/fan-shop/sp?view=all',
                  'https://www.hsn.com/shop/toys-and-games/ty?view=all',
                  'https://www.hsn.com/shop/coins-and-collectibles/co?view=all',
                  ]

    def parse(self, response):
        links = response.xpath('//div[not(@*)]/a/@href').extract()
        for item in links:
            yield response.follow(item, self.parse_item)
        next_page = response.xpath('//*[@id="template-product-grid"]/div[1]/div[2]/div[2]/div[2]/div/nav/ul/li[2]/a/@href').extract_first(default='null')
        if next_page != 'null':
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse, dont_filter = True)

    def parse_item(self, response):
        global count
        next_review_page = response.xpath('//*[@id="product-detail-reviews"]/div[3]/div/nav/ul/li[1]/@href').extract_first(default='null')
        data = {}
        for i in response.xpath('//tr[not(@*)]/td/text()').extract():
            if i.strip() != "":
                try:
                    data[i.strip()] = response.xpath('//tr[not(@*)]/td/span/text()').extract()[count].strip()
                    count+=1
                except IndexError:
                    data="No Description Found"
        count=0
        json_data = json.dumps(data)
        overview = response.xpath('//*[@id="overview"]/div/div/div/div/p/text()').extract()
        overview=list((item.strip() if hasattr(item, 'strip') else item for item in overview))
        overview=list(filter(None, overview))
        if len(overview) == 0:
            overview = ["No overview found."]
        yield {
            'product_category': response.xpath('//*[@id="breadcrumb"]/ol/li[2]/a/span/text()').extract_first(default='null'),
            'name': response.xpath('//*[@id="product-name"]/text()').extract_first(default='null'),
            'overview': overview[0],
            'imageURL' : response.xpath('//*[@id="template-product-detail-product"]/div[1]/div[2]/div[1]/a/img/@src').extract_first(default="null"),
            'price': response.xpath('//*[@id="template-product-detail-product"]/div[2]/div[2]/div[1]/div[1]/div/span[1]/text()').extract_first(default='null') + response.xpath('//*[@id="template-product-detail-product"]/div[2]/div[2]/div[1]/div[1]/div/span[2]/text()').extract_first(default='null'),
            'savings': response.xpath('//*[@id="template-product-detail-product"]/div[2]/div[2]/div[2]/div[2]/span/text()').extract_first(default='null'),
            'altPayment': response.xpath('//*[@id="template-product-detail-product"]/div[2]/div[2]/div[1]/div[2]/text()').extract_first(default='null').strip() + " * " + response.xpath('//*[@id="template-product-detail-product"]/div[2]/div[3]/form/div[3]/p/label/a/text()').extract_first(default='null').strip(),
            'giftEligibility': response.xpath('//*[@id="template-product-detail-product"]/div[2]/div[3]/form/p[1]/span/@data-tooltip').extract_first(default='null'),
            'productDesc': json_data,
            'noOfReviews': response.xpath('//*[@id="product-detail-reviews"]/div[1]/div[1]/div[2]/span/text()').extract_first(default='null').strip(),
            'rating': response.xpath('//*[@id="product-detail-reviews"]/div[1]/div[1]/div[2]/span/span/text()').extract_first(default='null').strip(),
            'review': response.xpath('//div[@class="copy"]/p/text()').extract(),
        }
        
