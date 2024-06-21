from typing import Iterable
import scrapy
from scrapy import Request

class LamarelSpider(scrapy.Spider):
    name = "lamarel_spider"
    start_urls = ['https://shoplamarel.com/']

    custom_settings = {
        'FEEDS': {'data.csv': {'format': 'csv'}}
    }

    def start_requests(self) -> Iterable[Request]:
        yield Request(url=self.start_urls[0], callback=self.parse_categories)

    def parse_categories(self, response):
        category_links = response.xpath('//details[@id="Details-HeaderMenu-1"]//ul//li//a/@href').getall()
        
        for link in category_links:
            url = response.urljoin(link)
            yield Request(url=url, callback=self.parse_category)

    def parse_category(self, response):
        product_links = response.xpath('//div[@class="card__information"]//a/@href').getall()
        
        for link in product_links:
            url = response.urljoin(link)
            yield Request(url=url, callback=self.parse_product)

    def parse_product(self, response):
        product_name = response.xpath('//div[@class="product__title"]//h1/text()').getall()
        image=response.xpath('//div[@class="product__media media media--transparent"]//img/@src').get()
        price=[price.strip() for price in response.xpath('//div[@class="price__regular"]//span[@class="price-item price-item--regular"]/text()').getall()]
        color=response.xpath('//legend//label[@class="swatch-label swatch-label-custom-image"]//span[@class="swatch-variant-name"]/text()').getall()
        size = response.xpath('//div[@class="swatch-button-title-text"]//span[@swatch-inside="true"]/text()').getall()
        description = [description.strip() for description in response.xpath('//div[@class="product__description rte quick-add-hidden"]//p[@data-mce-fragment="1"]/text()').getall()]
       
        yield {
            'productName': product_name,
            'image': image,
            'price': price,
            'color':color,
            'size':size,
            'description':description
        }

