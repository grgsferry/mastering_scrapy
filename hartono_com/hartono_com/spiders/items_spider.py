from pathlib import Path
import scrapy
class ItemsSpider(scrapy.Spider):
    name = "hartono_items"
    allowed_domains = ['myhartono.com']
    start_urls = [
        "https://myhartono.com/index.php?dispatch=categories.brand_pilihan&id=7&show_item_name=0",
    ]

    def parse(self, response):
        brand_urls = response.css('div.ty-column6 a::attr(href)').getall()
        # brand_urls = ['https://myhartono.com/en/aqua/']

        for brand_url in brand_urls:
            yield scrapy.Request(brand_url, callback=self.find_list_item)
    
    def find_list_item(self, response):
        item_urls = response.css('div.ty-grid-list__image > a::attr(href)').getall()

        next_page = response.css('a.ty-pagination__right-arrow::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.find_list_item)

        for item_url in item_urls:
            yield scrapy.Request(item_url, callback=self.find_detail_item)
    
    def find_detail_item(self, response):
        item = {
            'product_title': response.css('h1.ty-product-block-title bdi::text').get(),
            'product_sku': response.css('span.title_product_code::text').get(),
            'old_price': response.css('span.mh-old-price::text').getall()[3],
            'new_price': response.css('span.ty-price-num::text').getall()[1],
            'url': response.request.url
        }
        yield item