import pymysql
import scrapy

from ..items import HouseLinkItem


class HouseLinksSpider(scrapy.Spider):
    name = "HouseLinksSpider"
    allowed_domains = ["lianjia.com"]

    def start_requests(self):
        db = pymysql.connect(host='localhost',
                             port=3306,
                             user='root',
                             passwd='632632',
                             database='housing_evaluation')
        cursor = db.cursor()
        sql = "SELECT place_link, max_page FROM place_links;"
        cursor.execute(sql)
        result = cursor.fetchall()
        for row in result:
            max_page = row[1]
            for i in range(1, max_page + 1):
                yield scrapy.Request(url="https://bj.lianjia.com/" + row[0] + "pg" + str(i) + "/")

    def parse(self, response):
        place_name = response.xpath('/html/body/div[3]/div[1]/dl[2]/dd/div/div[2]/a[@class="selected"]/text()').extract()[0]
        for sel in response.xpath('/html/body/div[5]/div[1]/ul[@class="listContent"]/li'):
            houseLinkItem = HouseLinkItem()
            houseLinkItem['house_title'] = sel.xpath('./div[@class="info"]/div[@class="title"]/a/text()').extract()[0]
            houseLinkItem['house_link'] = sel.xpath('./div[@class="info"]/div[@class="title"]/a//@href').extract()[0]
            houseLinkItem['house_place_name'] = place_name
            yield houseLinkItem
