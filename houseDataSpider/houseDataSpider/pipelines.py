# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql

from .items import HouseLinkItem, PlaceLinkItem, PlaceMaxPageItem


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
            self.sql = "INSERT INTO house_links (house_title, house_link) VALUES (%s, %s);"
            try:
                self.cursor.execute(self.sql, (item['house_title'], item['house_link']))
                print("successfully insert!")
            except pymysql.Error:
                self.db.rollback()
                print(f"Wrong Here! With sql: '{self.sql}' item:\ntitle: {item['house_title']}\nlink: {item['house_link']}")

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
            self.sql = "INSERT INTO place_links (place_name, place_link) VALUES (%s, %s);"
            try:
                self.cursor.execute(self.sql, (item['place_name'], item['place_link']))
                print("successfully insert!")
            except pymysql.Error:
                self.db.rollback()
                print(
                    f"Wrong Here! With sql: '{self.sql}' item:\ntitle: {item['place_name']}\nlink: {item['place_link']}")

        return item

    def close_spider(self, spider):
        self.db.commit()
        self.cursor.close()
        self.db.close()
