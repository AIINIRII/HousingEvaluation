# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql

from .items import HouseLinkItem, PlaceLinkItem, PlaceMaxPageItem, HouseDataItem


class HouseLinksSpiderPipeline(object):

    def __init__(self):
        self.db = None
        self.cursor = None
        self.sql = ""

    def open_spider(self, spider):
        self.db = pymysql.connect(host='localhost',
                                  port=3306,
                                  user='root',
                                  passwd='632632',
                                  database='housing_evaluation')
        self.cursor = self.db.cursor()

    def process_item(self, item, spider):

        if isinstance(item, HouseLinkItem):
            self.sql = "INSERT INTO house_links (house_title, house_link, place_name) VALUES (%s, %s, %s);"
            try:
                self.cursor.execute(self.sql, (item['house_title'], item['house_link'], item['house_place_name']))
                print("successfully insert!")
            except pymysql.Error:
                self.db.rollback()
                print(
                    f"Wrong Here! With sql: '{self.sql}' item:\ntitle: {item['house_title']}\nlink: {item['house_link']}")

        if isinstance(item, PlaceLinkItem):
            self.sql = "INSERT INTO place_links (place_name, place_link) VALUES (%s, %s);"
            try:
                self.cursor.execute(self.sql, (item['place_name'], item['place_link']))
                print("successfully insert!")
            except pymysql.Error:
                self.db.rollback()
                print(
                    f"Wrong Here! With sql: '{self.sql}' item:\ntitle: {item['place_name']}\nlink: {item['place_link']}")

        if isinstance(item, PlaceMaxPageItem):
            self.sql = "UPDATE place_links SET max_page = %s WHERE place_link = %s;"
            try:
                self.cursor.execute(self.sql, (item['place_maxPage'], item['place_link']))
                print("successfully insert!")
            except pymysql.Error:
                self.db.rollback()
                print(
                    f"Wrong Here! With sql: '{self.sql}' item:\nplace_maxPage: {item['place_maxPage']}\nplace_link: {item['place_link']}")

        if isinstance(item, HouseDataItem):
            self.sql = "INSERT INTO house_info (house_title, house_floor, house_price, house_type, house_finish, " \
                       "house_area, house_towards, have_elevator, elevator_ratio, completion_time, trading_date) " \
                       "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
            try:
                self.cursor.execute(self.sql, (
                    item['house_title'], item['house_floor'], item['house_price'], item['house_type'],
                    item['house_finish'], item['house_area'], item['house_towards'], item['have_elevator'],
                    item['elevator_ratio'], item['completion_time'], item['trading_date']))
                print("successfully insert!")
            except pymysql.Error:
                self.db.rollback()
                print(
                    f"Wrong Here! With sql: '{self.sql}' item:\nplace_maxPage: {item['place_maxPage']}\nplace_link: {item['place_link']}")

        return item

    def close_spider(self, spider):
        self.db.commit()
        self.cursor.close()
        self.db.close()
