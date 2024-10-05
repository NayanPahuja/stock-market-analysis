from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from . import crud, models, schemas
from .database import SessionLocal, engine
from .tasks import process_stock_data

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/ingest_stock_data/", response_model=schemas.StockData)
def ingest_stock_data(stock_data: schemas.StockDataCreate, db: Session = Depends(get_db)):
    db_stock_data = crud.create_stock_data(db=db, stock_data=stock_data)
    process_stock_data.delay(db_stock_data.id)
    return db_stock_data

@app.get("/stock_data/{stock_symbol}", response_model=list[schemas.StockData])
def read_stock_data(stock_symbol: str, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    stock_data = crud.get_stock_data_by_symbol(db, stock_symbol=stock_symbol, skip=skip, limit=limit)
    return stock_data

@app.get("/analysis/{stock_symbol}", response_model=schemas.StockAnalysis)
def read_stock_analysis(stock_symbol: str, db: Session = Depends(get_db)):
    analysis = crud.get_stock_analysis(db, stock_symbol=stock_symbol)
    if analysis is None:
        raise HTTPException(status_code=404, detail="Analysis not found")
    return analysis
