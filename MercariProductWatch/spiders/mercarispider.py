import scrapy
import logging
from MercariProductWatch.database import mercariproductwatchdb
from MercariProductWatch.database.models import Products, WatchLinks

from datetime import datetime
import time

from MercariProductWatch.items import ProductItem
now = datetime.now()

timestr = time.strftime("%Y%m%d-%H%M%S")

link_log= logging.getLogger("link_log")
hdlr = logging.FileHandler(f'links.log', mode="a")
link_log.addHandler(hdlr)
link_log.setLevel(logging.INFO)
# link_log.propagate = False
link_log.info("***************" + str(now) + "***************")

logging.basicConfig(level=logging.INFO)
logging.getLogger('scrapy').propagate = False

class MercariSpider(scrapy.Spider):
    name = "mercarispider"
    db = mercariproductwatchdb.MercariProductWatchDatabase()

    def start_requests(self):
        # s = self.db.session.query(Categories).all()
        for link in self.db.session.query(WatchLinks).all():
            yield scrapy.Request(url=link.url, callback=self.parse_watchlink, meta={'watchlink_id':link.id}, priority=0)
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

        for item in response.xpath('//section[@class="items-box"]'):
            product_url = item.xpath('./a/@href').extract()[0].split(r"/?_s")[0]
            product_image_url = item.xpath('./a/figure/img/@data-src').extract()[0]
            name = item.xpath('./a/div/h3/text()').extract()[0]
            price = item.xpath('./a/div').css('.items-box-body').css('.items-box-num').css('.items-box-price').xpath('./text()').extract()[0]
            logging.debug(f'item: {name} - price: {price}')
            yield ProductItem(product_url = product_url, product_image_url = product_image_url, name = name, price = price)
