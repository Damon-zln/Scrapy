# -*- coding: utf-8 -*-
from scrapy import Request, Spider
from urllib.parse import quote
from taobao_selenium.items import ProductItem


class TaobaoSpider(Spider):
    name = 'taobao'
    allowed_domains = ['www.taobao.com']
    base_url = 'https://s.taobao.com/search?q='

    def start_requests(self):
        for keyword in self.settings.get('KEYWORDS'):
            for page in range(1, self.settings.get('MAX_PAGE') + 1):
                url = self.base_url + quote(keyword)
                yield Request(url=url, callback=self.parse, meta={'page': page}, dont_filter=True)

    def parse(self, response):
        products = response.xpath('//div[@id="mainsrp-itemlist"]//div[@class="items"][1]//div[contains(@class, "item")]')
        for product in products:
            item = ProductItem()
            item['image'] = ''.join(product.xpath('.//div[@class="pic"]//img[contains(@class, "img")]/@data-src').extract()).strip()
            item['price'] = ''.join(product.xpath('.//div[contains(@class, "price")]//text()').extract()).strip()
            item['deal'] = ''.join(product.xpath('.//div[@class="deal-cnt"]//text()').extract_first()).strip()
            item['title'] = ''.join(product.xpath('.//div[contains(@class, "title")]//text()').extract()).strip()
            item['shop'] = ''.join(product.xpath('.//div[@class="shop"]//text()').extract()).strip()
            item['location'] = ''.join(product.xpath('.//div[@class="location"]//text()').extract_first()).strip()
            yield item
