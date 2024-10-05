from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class StockData(Base):
    __tablename__ = "stock_data"

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, index=True)
    price = Column(Float)
    timestamp = Column(DateTime)

class StockAnalysis(Base):
    __tablename__ = "stock_analysis"

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, index=True)
    average_price = Column(Float)
    price_change = Column(Float)
    timestamp = Column(DateTime)