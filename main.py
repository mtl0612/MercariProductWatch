from mercariproductwatchdb import MercariProductWatchDatabase
from models import WatchLinks, Product
import logging

db = MercariProductWatchDatabase()
for watchlink in db.session.query(WatchLinks).all():
    logging.debug(watchlink.url)