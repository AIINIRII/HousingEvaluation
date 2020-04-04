import scrapy

from ..items import HouseLinkItem


class HouseLinksSpider(scrapy.Spider):
    name = "HouseLinksSpider"
    allowed_domains = ["lianjia.com"]
    start_urls = ["https://bj.lianjia.com/chengjiao/"]

    def parse(self, response):
        for sel in response.xpath('/html/body/div[5]/div[1]/ul[@class="listContent"]/li'):
            houseLinkItem = HouseLinkItem()
            houseLinkItem['house_title'] = sel.xpath('./div[@class="info"]/div[@class="title"]/a/text()').extract()[0]
            houseLinkItem['house_link'] = sel.xpath('./div[@class="info"]/div[@class="title"]/a//@href').extract()[0]
            yield houseLinkItem
