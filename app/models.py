from sqlalchemy import Column, String, Integer, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Product(Base):
    __tablename__ = "products"

    artikul = Column(String, primary_key=True, index=True)
    name = Column(String, index=True)
    price = Column(Float)
    rating = Column(Float)
    stock_count = Column(Integer)
