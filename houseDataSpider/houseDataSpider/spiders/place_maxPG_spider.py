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

        placeMaxPageItem['place_maxPage'] = \
            response.xpath('/html/body/div[5]/div[1]/div[5]/div[2]/div/@page-data').extract()[0].split(
                "\"totalPage\":")[1].split(",")[0]
        placeMaxPageItem['place_link'] = \
            response.xpath('/html/body/div[5]/div[1]/div[5]/div[2]/div/@page-url').extract()[0].split("pg")[0]

        yield placeMaxPageItem
