# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Item, Field


class HSNItem(Item):
    # define the fields for your item here like:
    # name = Field()
    name = Field()
    price = Field()
    productDesc = Field()
    savings = Field()
    salePrice = Field()
    altPayment = Field()
    rating = Field()
    review = Field()
    noOfReviews = Field()
    noOfRatings = Field()
    colour = Field()
    careLabel = Field()
    material = Field()
    xSmall = Field()
    small = Field()
    medium = Field()
    large = Field()
    xLarge = Field()
    cashOnDelivery = Field()
    giftEligibility = Field()
    delivery_above_forty = Field()
    deliver_date = Field()
    
