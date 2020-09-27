import scrapy
import logging
from MercariProductWatch.database import mercariproductwatchdb
from MercariProductWatch.database.models import Products, WatchLinks, Options

from datetime import datetime
import time
import os
from MercariProductWatch.items import ProductItem
from pathlib import Path
from urllib.parse import urlparse

from MercariProductWatch.slackbot import SlackBot
import html

VERSION = "0.0.2"

now = datetime.now()
timestr = time.strftime("%Y%m%d-%H%M%S")

link_log= logging.getLogger("link_log")
log_loc = Path(os.getcwd()).parent / 'logs'
hdlr = logging.FileHandler(log_loc / 'links.log', mode="a")
link_log.addHandler(hdlr)
link_log.setLevel(logging.INFO)
link_log.propagate = False
link_log.info("***************" + str(now) + "***************")

request_log = logging.getLogger("requests")
request_log.setLevel(logging.INFO)
request_log.propagate = False

logging.basicConfig(level=logging.INFO)
logging.getLogger('scrapy').propagate = False
logging.getLogger('scrapy').setLevel(logging.INFO)

logging.info(f"mercarispider version: {VERSION}")
class MercariSpider(scrapy.Spider):
    name = "mercarispider"
    db = mercariproductwatchdb.MercariProductWatchDatabase()
    bot = SlackBot()
    def start_requests(self):
        self.db.create_db_tables()
        # s = self.db.session.query(Categories).all()
        slack_ts = self.db.session.query(Options).filter(Options.name == "slack_ts").first()
        if slack_ts is None:
            slack_ts = Options('slack_ts', None)
        new_ts = slack_ts.value
        for message in self.bot.receive_message(slack_ts.value):
            current_ts = message['ts']
            if new_ts is None:
                new_ts = current_ts
            if float(current_ts) > float(new_ts):
                new_ts = current_ts
            if 'bot_id' not in message and message['text'].lower().startswith('add'):
                split_message_text = html.unescape(message['text']).split()
                url = split_message_text[1][1:-1]
                if len(split_message_text) > 2:
                    name =' '.join(split_message_text[2:])
                else:
                    name = None
                url_parsed = urlparse(url)
                if url_parsed.scheme in ['http', 'https'] and url_parsed.netloc != '':
                    self.db.add_watch_url(name, url)
        slack_ts.value = new_ts
        self.db.session.add(slack_ts)
        self.db.session.commit()
        for link in self.db.session.query(WatchLinks).all():
            yield scrapy.Request(url=link.url, callback=self.parse_watchlink, 
                                 meta={'watchlink_id':link.id, 'watchlink_name':link.name }, 
                                 priority=0)

    def parse_watchlink(self, response):
        url = response.url
        link_log.info(url)
        try:
            search_result_description = response.xpath('//p[@class="search-result-description"]').extract()[0]
            logging.debug(search_result_description)
            if "該当する商品が見つかりません" in search_result_description:
                logging.info(f"No product found in {url}")
                return
        except IndexError:
            pass
        n_item = 0
        for item in response.xpath('//section[@class="items-box"]'):
            if n_item > 20:
                return
            n_item +=1
            product_url = item.xpath('./a/@href').extract()[0].split(r"/?_s")[0]
            product_image_url = item.xpath('./a/figure/img/@data-src').extract()[0]
            name = item.xpath('./a/div/h3/text()').extract()[0]
            price = item.xpath('./a/div').css('.items-box-body').css('.items-box-num')\
                        .css('.items-box-price').xpath('./text()').extract()[0]
            logging.debug(f'item: {name} - price: {price}')
            watchlink_name = response.meta['watchlink_name']
            yield ProductItem(product_url = product_url, product_image_url = product_image_url, 
                              name = name, price = price, watchlink_name = watchlink_name)
