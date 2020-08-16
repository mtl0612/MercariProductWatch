# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MercariproductwatchItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class ProductItem(scrapy.Item):
    product_url = scrapy.Field()
    product_image_url = scrapy.Field()
    name = scrapy.Field()
    price = scrapy.Field()

    def __repr__(self):
        return repr({"ProductItem url: ": self['product_url']})
