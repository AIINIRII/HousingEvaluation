import pymysql
import scrapy

from ..items import PlaceMaxPageItem


class PlaceMaxPageSpider(scrapy.Spider):
    name = "PlaceMaxPageSpider"
    allowed_domains = ["lianjia.com"]

    def start_requests(self):
        db = pymysql.connect(host='localhost',
                             port=3306,
                             user='root',
                             passwd='632632',
                             database='housing_evaluation')
        cursor = db.cursor()
        sql = "SELECT place_link FROM place_links;"
        cursor.execute(sql)
        result = cursor.fetchall()
        for row in result:
            yield scrapy.Request(url="https://bj.lianjia.com/" + row[0])

    def parse(self, response):
        placeMaxPageItem = PlaceMaxPageItem()
        placeMaxPageItem['place_maxPage'] = response.xpath('/html/body/div[5]/div[1]/div[5]/div[2]/div/a[4]').extract()[
            0]
        placeMaxPageItem['place_name'] = ""  # TODO
        placeMaxPageItem['place_link'] = ""
        yield placeMaxPageItem
