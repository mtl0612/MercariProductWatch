from MercariProductWatch.database.mercariproductwatchdb import MercariProductWatchDatabase
SQLITE = 'sqlite'
if __name__ == "__main__":
    db = MercariProductWatchDatabase(SQLITE)
    db.create_db_tables()
    db.insert_categories()
    db.print_categories()