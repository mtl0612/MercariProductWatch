from MercariProductWatch.database.models import Base
from MercariProductWatch.database.models import WatchLinks
from sqlalchemy import create_engine
from sqlalchemy import MetaData
from sqlalchemy.orm import sessionmaker

import logging
import os

logging.basicConfig(level=logging.DEBUG)

# logger = logging.getLogger(__name__)
SQLITE = 'sqlite'
#Table Names

class MercariProductWatchDatabase:
    DB_ENGINE = {
        'sqlite' : 'sqlite:///{DB}'
    }

    #Main DB Connection Ref Obj
    db_engine = None
    def __init__(self, dbtype='sqlite', username='', password='', dbname='mercariproductwatch.db'):
        dbtype = dbtype.lower()
        logging.debug('dbtype is %s' % dbtype)
        if dbtype in self.DB_ENGINE.keys():
            db_path = os.path.join(os.path.dirname(__file__), dbname)
            engine_url = self.DB_ENGINE[dbtype].format(DB=db_path)
            logging.debug("engine_url is %s" %engine_url)
            self.db_engine = create_engine(engine_url)
            logging.debug(self.db_engine)
            self.metadata = MetaData()
            Session = sessionmaker(bind=self.db_engine)
            self.session = Session()
        else:
            print("DBType is not found in DB_ENGINE")
    def create_db_tables(self):
        try:
            Base.metadata.create_all(self.db_engine)
        except Exception as e:
            print("Error occurred during Table creation!")
            print(e)

    def insert_categories(self):
        links = [
            WatchLinks('Fujifilm 50 230', r"https://www.mercari.com/jp/search/?sort_order=&keyword=fujifilm+50+230&category_root=&brand_name=&brand_id=&size_group=&price_min=&price_max=20000&status_on_sale=1"),
        ]
        for link in links:
            if self.session.query(WatchLinks).filter(WatchLinks.url == link.url).first() is None:
                self.session.add(link)
        self.session.commit()
        
    def print_categories(self):
        results = self.session.query(WatchLinks)
        for row in results:
            print(row)
if __name__ == "__main__":
    db = MercariProductWatchDatabase(SQLITE)
    db.create_db_tables()
    db.insert_categories()
    db.print_categories()