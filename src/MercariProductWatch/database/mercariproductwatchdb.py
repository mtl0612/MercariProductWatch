from MercariProductWatch.database.models import Base
from MercariProductWatch.database.models import WatchLinks
from sqlalchemy import create_engine
from sqlalchemy import MetaData
from sqlalchemy.orm import sessionmaker

import logging
import os
from pathlib import Path

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
            db_src = Path(os.getcwd())
            db_store_loc = db_src.parent / 'database'
            db_path = os.path.join(db_store_loc, dbname)
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
    
    def add_watch_url(self, name,url):
        if self.session.query(WatchLinks).filter(WatchLinks.url == url).first() is None:
            new_watch_link = WatchLinks(name, url)
            self.session.add(new_watch_link)
            self.session.commit()
# if __name__ == "__main__":
    # db = MercariProductWatchDatabase(SQLITE)
    # db.create_db_tables()
    # db.insert_categories()
    # db.print_categories()