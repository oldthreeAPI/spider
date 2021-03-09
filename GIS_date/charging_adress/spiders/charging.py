"""
爬取广东地区所有充电桩的分布信息，地址，站名，快充慢充，数量等
"""

import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class ChargingSpider(CrawlSpider):
    name = 'charging'
    allowed_domains = ['admin.bjev520.com']
    start_urls = ['http://admin.bjev520.com/jsp/beiqi/pcmap/pages/pcmap_Left.jsp?cityName=%E5%B9%BF%E4%B8%9']

    rules = (
        Rule(LinkExtractor(allow=r'/jsp/beiqi/pcmap/do/pcmap_Detail\.jsp\?charingId=\d+'), callback='parse_item'),
    )

    def start_requests(self):
        cookies = {
            "JSESSIONID": "52FC90F1397EE87DDB81A22C5770A7A4"
        }
        yield scrapy.Request(
            self.start_urls[0],
            cookies=cookies,
        )

    def parse_item(self, response):
        item = {}
        item["name"] = response.xpath('//div[@class="news-l"/div[@class="news-top"]]/p/text()').extract_first()
        item["adress"] = response.xpath('div[@class="news-l"]/div[@class="news-con"]/div[@class="news-a"]/p/text()').extract_first()
        item["type"] = response.xpath('div[@class="news-l"]/div[@class="news-c"]/span/text()').extract_first()
        item["class"] = response.xpath('div[@class="news-l"]/div[@class="news-c"]/em/text()').extract()[0]
        yield item