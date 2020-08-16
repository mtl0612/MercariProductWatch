# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

from MercariProductWatch.database import mercariproductwatchdb
from MercariProductWatch.database.models import Products, WatchLinks
import logging
from MercariProductWatch.slackbot import SlackBot

class MercariproductwatchPipeline:

    db = mercariproductwatchdb.MercariProductWatchDatabase()
    bot = SlackBot()

    def process_item(self, item, spider):
        product_id = int(item['product_url'].split("/")[-1][1::]) 
        product = self.db.session.query(Products).filter(Products.product_id ==product_id).first()
        if product is None:
            logging.info(f'Product id {product_id} not existed in database!')
            name = item['name']
            url = item['product_url']
            product_image_url = item['product_image_url']
            price = int(item['price'][1::].replace(',',''))
            product = Products(product_id = product_id, name = name, url = url, product_image_url = product_image_url, price = price)
            self.db.session.add(product)
            self.db.session.commit()
            self.bot.send_message(f'Product name: {name}\nPrice: {price}\nUrl: {"https://www.mercari.com" + url}\n\n')
            
        return item
