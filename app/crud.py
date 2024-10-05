from sqlalchemy.orm import Session
from . import models, schemas

def create_stock_data(db: Session, stock_data: schemas.StockDataCreate):
    db_stock_data = models.StockData(**stock_data.model_dump())
    db.add(db_stock_data)
    db.commit()
    db.refresh(db_stock_data)
    return db_stock_data

def get_stock_data_by_symbol(db: Session, stock_symbol: str, skip: int = 0, limit: int = 100):
    return db.query(models.StockData).filter(models.StockData.symbol == stock_symbol).offset(skip).limit(limit).all()

def get_stock_analysis(db: Session, stock_symbol: str):
    return db.query(models.StockAnalysis).filter(models.StockAnalysis.symbol == stock_symbol).first()

def create_stock_analysis(db: Session, stock_analysis: schemas.StockAnalysisCreate):
    db_stock_analysis = models.StockAnalysis(**stock_analysis.model_dump())
    db.add(db_stock_analysis)
    db.commit()
    db.refresh(db_stock_analysis)
    return db_stock_analysis