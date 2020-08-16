from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Table, Column, Integer,Float, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

Base = declarative_base()

# association table
watchlink_product = Table('watchlink_product', Base.metadata,
    Column('watchlink_id', Integer, ForeignKey('watchlinks.id')),
    Column('product_id', Integer, ForeignKey('products.id'))
)

class WatchLinks(Base):
    __tablename__ = 'watchlinks'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    url = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    def __init__(self, name, url):
        self.name = name
        self.url = url

    def __repr__(self):
        return "<Links('%s','%s')>" % (self.name, self.url)

class Products(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True)
    product_id = Column(Integer)
    name = Column(String)
    url = Column(String)
    product_image_url = Column(String)
    price = Column(Float)
    links = relationship("WatchLinks", secondary=watchlink_product, backref='watchlinks')
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    def __init__(self, product_id, name, url, product_image_url, price):
        self.name = name
        self.url = url
        self.product_id = product_id
        self.price = price

    def __repr__(self):
        return "<Product('%s','%s')>" % (self.name, self.url)