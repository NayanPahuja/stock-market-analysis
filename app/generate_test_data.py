import requests
import random
from datetime import datetime, timedelta

BASE_URL = "http://localhost:8000"

def generate_stock_price(base_price, volatility):
    change_percent = volatility * (random.random() - 0.5)
    return base_price * (1 + change_percent)

def generate_comparison_data(symbols, days, base_prices, volatilities):
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    
    current_date = start_date
    while current_date <= end_date:
        for minute in range(0, 1440, 5):  # Generate data every 5 minutes
            current_time = current_date + timedelta(minutes=minute)
            timestamp = current_time.isoformat()
            
            for symbol, base_price, volatility in zip(symbols, base_prices, volatilities):
                current_price = generate_stock_price(base_price, volatility)
                base_price = current_price  # Update base price for next iteration
                
                data = {
                    "symbol": symbol,
                    "price": round(current_price, 2),
                    "timestamp": timestamp
                }
                
                response = requests.post(f"{BASE_URL}/ingest_stock_data/", json=data)
                if response.status_code == 200:
                    print(f"Successfuly ingested data for {symbol}: {data}")
                else:
                    print(f"Failed to ingest data: {response.text}")
        
        current_date += timedelta(days=1)

if __name__ == "__main__":
    symbols = ["AAPL", "GOOGL", "MSFT", "AMZN", "TSLA"]
    base_prices = [150, 2800, 300, 3300, 700]
    volatilities = [0.001, 0.0012, 0.0009, 0.0015, 0.002]
    
    generate_comparison_data(symbols, days=7, base_prices=base_prices, volatilities=volatilities)