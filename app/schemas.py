from pydantic import BaseModel
from datetime import datetime

class StockDataBase(BaseModel):
    symbol: str
    price: float
    timestamp: datetime

class StockDataCreate(StockDataBase):
    pass

class StockData(StockDataBase):
    id: int

    class Config:
        orm_mode = True

class StockAnalysisBase(BaseModel):
    symbol: str
    average_price: float
    price_change: float
    timestamp: datetime

class StockAnalysisCreate(StockAnalysisBase):
    pass

class StockAnalysis(StockAnalysisBase):
    id: int

    class Config:
        orm_mode = True