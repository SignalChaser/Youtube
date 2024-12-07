import yfinance as yf
import csv
import os
from datetime import datetime, timedelta

# Define directories
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Base directory
CRYPTO_TICKERS_DIR = os.path.join(BASE_DIR, "crypto_tickers")  # Folder for tickers list
CRYPTO_DATA_DIR = os.path.join(BASE_DIR, "crypto_data")  # Folder for storing data

# Ensure the data storage directory exists
if not os.path.exists(CRYPTO_DATA_DIR):
    os.makedirs(CRYPTO_DATA_DIR)
    print(f"Created directory for data: {CRYPTO_DATA_DIR}")

def get_crypto_list():
    """Read the crypto list from the tickers folder"""
    try:
        crypto_list = []
        csv_file = os.path.join(CRYPTO_TICKERS_DIR, "top_crypto_list.csv")
        print(f"Looking for CSV file at: {csv_file}")
        
        if not os.path.exists(csv_file):
            print(f"CSV file not found at: {csv_file}")
            return []
            
        with open(csv_file, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                crypto_list.append(row['symbol'])
        print(f"Found {len(crypto_list)} cryptocurrencies")
        return crypto_list
    except Exception as e:
        print(f"Error reading crypto list: {e}")
        return []

def fetch_historical_data(symbol, start_time, end_time):
    """Fetch historical hourly data for a given crypto symbol"""
    try:
        ticker = yf.Ticker(symbol)
        df = ticker.history(start=start_time, end=end_time, interval='1h')
        
        if df.empty:
            print(f"No data returned for {symbol}")
            return []
            
        data = [(t.strftime("%Y-%m-%d %H:%M:%S"), price) 
                for t, price in zip(df.index, df['Close'])]
        return data
    except Exception as e:
        print(f"Error fetching historical data for {symbol}: {e}")
        return []

def save_to_csv(symbol, data):
    """Save the crypto data to the data storage folder"""
    try:
        filename = f"{symbol.lower().replace('-', '_')}_hourly_data.csv"
        csv_file = os.path.join(CRYPTO_DATA_DIR, filename)  # Data storage directory
        
        with open(csv_file, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["timestamp", "price_usd"])  # Header
            writer.writerows(data)
        print(f"Successfully saved data for {symbol}")
    except Exception as e:
        print(f"Error saving data for {symbol}: {e}")

def update_data():
    """Main function to update all crypto data"""
    print(f"Starting crypto data update at {datetime.now()}")
    
    # Get list of cryptocurrencies from our CoinGecko CSV
    cryptos = get_crypto_list()
    if not cryptos:
        print("No cryptocurrencies found in list!")
        return
    
    # Calculate time range - last 30 days
    end_time = datetime.now()
    start_time = end_time - timedelta(days=30)
    
    # Fetch and save data for each crypto
    for symbol in cryptos:
        print(f"Fetching data for {symbol}")
        historical_data = fetch_historical_data(symbol, start_time, end_time)
        if historical_data:
            save_to_csv(symbol, historical_data)
        else:
            print(f"No data to save for {symbol}")

if __name__ == "__main__":
    update_data()
