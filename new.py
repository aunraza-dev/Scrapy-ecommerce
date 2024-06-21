    def parse_category_page(self, response):
        product_links = response.xpath('//div[@class="product-grid-container scroll-trigger animate--slide-in")]/@href').getall()

        for link in product_links:
            if link.startswith('/'):
                link = response.urljoin(link)
            yield Request(url=link, callback=self.parse_product_page)