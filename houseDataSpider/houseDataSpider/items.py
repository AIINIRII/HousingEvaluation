# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class HouseLinkItem(scrapy.Item):
    house_title = scrapy.Field()
    house_link = scrapy.Field()


class PlaceLinkItem(scrapy.Item):
    place_name = scrapy.Field()
    place_link = scrapy.Field()


class PlaceMaxPageItem(scrapy.Item):
    place_link = scrapy.Field()
    place_maxPage = scrapy.Field()


class HousedataspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    house_id = scrapy.Field()
    house_condition = scrapy.Field()
    house_title = scrapy.Field()
    house_location = scrapy.Field()
    house_floor = scrapy.Field()
    house_price = scrapy.Field()
    house_type = scrapy.Field()
    house_finish = scrapy.Field()
    house_area = scrapy.Field()
    house_towards = scrapy.Field()
    have_elevator = scrapy.Field()
    elevator_ratio = scrapy.Field()
    completion_time = scrapy.Field()
    trading_date = scrapy.Field()
