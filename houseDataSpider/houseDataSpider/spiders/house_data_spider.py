import pymysql
import scrapy

from ..items import HouseDataItem


class HouseDataSpider(scrapy.Spider):
    name = "HouseDataSpider"
    allowed_domains = ["lianjia.com"]

    def start_requests(self):
        db = pymysql.connect(host='localhost',
                             port=3306,
                             user='root',
                             passwd='632632',
                             database='housing_evaluation')
        cursor = db.cursor()
        sql = "SELECT DISTINCT house_link, house_id FROM house_links;"
        cursor.execute(sql)
        result = cursor.fetchall()
        for row in result:
            print(f"Now the house id is {row[1]}")
            yield scrapy.Request(url=row[0])

    def parse(self, response):
        houseDataItem = HouseDataItem()
        houseDataItem['house_title'] = response.xpath('/html/body/div[4]/div/text()').extract()[0].strip()
        houseDataItem['house_price'] = \
            response.xpath('/html/body/section[1]/div[2]/div[2]/div[1]/span/i/text()').extract()[0] + \
            response.xpath('/html/body/section[1]/div[2]/div[2]/div[1]/span/text()').extract()[0].strip()
        date_in_text = response.xpath('/html/body/div[4]/div/span/text()').extract()[0].strip()
        if date_in_text.split(" ")[1] == "成交":
            houseDataItem['trading_date'] = date_in_text.split(" ")[0].strip()
        houseDataItem['house_floor'] = \
            response.xpath('//*[@id="introduction"]/div[1]/div[1]/div[2]/ul/li[2]/text()').extract()[0].strip()
        houseDataItem['house_type'] = \
            response.xpath('//*[@id="introduction"]/div[1]/div[1]/div[2]/ul/li[6]/text()').extract()[0].strip()
        houseDataItem['house_finish'] = \
            response.xpath('//*[@id="introduction"]/div[1]/div[1]/div[2]/ul/li[8]/text()').extract()[0].strip()
        houseDataItem['house_area'] = \
            response.xpath('//*[@id="introduction"]/div[1]/div[1]/div[2]/ul/li[3]/text()').extract()[0].strip()
        houseDataItem['house_towards'] = \
            response.xpath('//*[@id="introduction"]/div[1]/div[1]/div[2]/ul/li[7]/text()').extract()[0].strip()
        houseDataItem['have_elevator'] = \
            response.xpath('//*[@id="introduction"]/div[1]/div[1]/div[2]/ul/li[14]/text()').extract()[0].strip()
        houseDataItem['elevator_ratio'] = \
            response.xpath('//*[@id="introduction"]/div[1]/div[1]/div[2]/ul/li[12]/text()').extract()[0].strip()
        houseDataItem['completion_time'] = \
            response.xpath('//*[@id="introduction"]/div[1]/div[1]/div[2]/ul/li[8]/text()').extract()[0].strip()
        yield houseDataItem
