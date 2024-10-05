from celery import Celery
from sqlalchemy.orm import Session
from .database import SessionLocal
from . import crud, models, schemas
from .config import RABBITMQ_URL

celery_app = Celery('tasks', broker=RABBITMQ_URL)

@celery_app.task
def process_stock_data(stock_data_id: int):
    db = SessionLocal()
    try:
        # Fetch the stock data
        stock_data = db.query(models.StockData).filter(models.StockData.id == stock_data_id).first()
        
        if stock_data:
            # Perform analysis
            symbol = stock_data.symbol
            
            # Get all stock data for this symbol
            all_stock_data = crud.get_stock_data_by_symbol(db, symbol)
            
            # Calculate average price
            average_price = sum(data.price for data in all_stock_data) / len(all_stock_data)
            
            # Calculate price change (assuming the list is ordered by timestamp)
            price_change = all_stock_data[-1].price - all_stock_data[0].price if len(all_stock_data) > 1 else 0
            
            # Create or update stock analysis
            analysis = crud.get_stock_analysis(db, symbol)
            if analysis:
                analysis.average_price = average_price
                analysis.price_change = price_change
                analysis.timestamp = stock_data.timestamp
            else:
                analysis_data = schemas.StockAnalysisCreate(
                    symbol=symbol,
                    average_price=average_price,
                    price_change=price_change,
                    timestamp=stock_data.timestamp
                )
                crud.create_stock_analysis(db, analysis_data)
            
            db.commit()
    finally:
        db.close()

# Make sure to export the celery_app
__all__ = ['celery_app']