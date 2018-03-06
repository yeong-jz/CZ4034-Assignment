# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Item, Field


class LazadaItem(Item):
    # define the fields for your item here like:
    # name = Field()

    name = Field()
    brand = Field()
    generalCat = Field()
    salePrice = Field()
    originalPrice = Field()
    rating = Field()
    noOfRatings = Field()
    positiveSellerRatings = Field()
    returnPolicy = Field()
    warranty = Field()
    economyDeliveryPrice = Field()
    standardDeliveryPrice = Field()
    expressDeliveryPrice = Field()
    
