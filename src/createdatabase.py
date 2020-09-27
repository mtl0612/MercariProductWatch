from MercariProductWatch.database.mercariproductwatchdb import MercariProductWatchDatabase
SQLITE = 'sqlite'
insert_categories(db):
    links = [
        WatchLinks('Fujifilm 50 230', r"https://www.mercari.com/jp/search/?sort_order=&keyword=fujifilm+50+230&category_root=&brand_name=&brand_id=&size_group=&price_min=&price_max=20000&status_on_sale=1"),
    ]
    for link in links:
        if db.session.query(WatchLinks).filter(WatchLinks.url == link.url).first() is None:
            db.session.add(link)
    db.session.commit()
    
print_categories(db):
    results = db.session.query(WatchLinks)
    for row in results:
        print(row)

if __name__ == "__main__":
    db = MercariProductWatchDatabase(SQLITE)
    db.create_db_tables()
    db.insert_categories(db)
    db.print_categories(db)