import scrapy

from ..items import PlaceLinkItem

places = ["dongcheng", "xicheng", "chaoyang", "haidian", "fengtai", "shijingshan", "tongzhou", "changping", "daxing",
          "yizhuangkaifaqu", "shunyi", "fangshan", "mentougou", "pinggu", "huairou", "miyun", "yanqing"]


class PlaceLinksSpider(scrapy.Spider):
    name = "PlaceLinksSpider"
    allowed_domains = ["lianjia.com"]
    start_urls = ["https://bj.lianjia.com/chengjiao/{}/".format(p) for p in places]

    def parse(self, response):
        for sel in response.xpath('/html/body/div[3]/div[1]/dl[2]/dd/div/div[2]/a'):
            placeLinkItem = PlaceLinkItem()
            placeLinkItem['place_name'] = sel.xpath('./text()').extract()[0]
            placeLinkItem['place_link'] = sel.xpath('./@href').extract()[0]
            yield placeLinkItem
