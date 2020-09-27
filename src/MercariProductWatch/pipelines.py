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
import time
import random

class MercariproductwatchPipeline:

    db = mercariproductwatchdb.MercariProductWatchDatabase()
    bot = SlackBot()

    def process_item(self, item, spider):
        name = item['name']
        product_id = int(item['product_url'].split("/")[-1][1::]) 
        price_on_web = int(item['price'][1::].replace(',',''))
        url = item['product_url']
        product = self.db.session.query(Products).filter(Products.product_id ==product_id).first()
        channel_id = self.bot.find_create_channel('mer_pro_' + item['watchlink_name'])
        if product is None:
            logging.info(f'Product id {product_id} not existed in database!')
            product_image_url = item['product_image_url']
            product = Products(product_id = product_id, name = name, url = url, product_image_url = product_image_url, price = price_on_web)
            self.db.session.add(product)
            self.db.session.commit()
            self.bot.send_message(f'Product name: {name}\nPrice: {price_on_web}\nUrl: {"https://www.mercari.com" + url}\n\n', channel_id)
        elif product.price != price_on_web:
            old_price = product.price
            product.price = price_on_web
            self.db.session.commit()
            self.bot.send_message(f'Product name: {name}\nPrice changed from {old_price} to {price_on_web}\nUrl: {"https://www.mercari.com" + url}\n\n', channel_id)
        return item
