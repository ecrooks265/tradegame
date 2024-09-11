
import sqlite3
import random

# Define sectors with baseline volatilities
SECTORS = {
    'TECH': {'volatility': (0.10, 0.25), 'growth_rate': (0.07, 0.15)},
    'FIN': {'volatility': (0.05, 0.15), 'growth_rate': (0.03, 0.08)},
    'HEALTH': {'volatility': (0.08, 0.20), 'growth_rate': (0.05, 0.12)},
    'CONS': {'volatility': (0.04, 0.12), 'growth_rate': (0.02, 0.06)},
    'ENERGY': {'volatility': (0.12, 0.30), 'growth_rate': (0.04, 0.10)},
}

# Example stocks to seed into the database
STOCKS = [
    {'name': 'AAPL', 'sector': 'TECH'},
    {'name': 'MSFT', 'sector': 'TECH'},
    {'name': 'GOOG', 'sector': 'TECH'},
    {'name': 'JPM', 'sector': 'FIN'},
    {'name': 'BAC', 'sector': 'FIN'},
    {'name': 'GS', 'sector': 'FIN'},
    {'name': 'PFE', 'sector': 'HEALTH'},
    {'name': 'JNJ', 'sector': 'HEALTH'},
    {'name': 'MRK', 'sector': 'HEALTH'},
    {'name': 'PG', 'sector': 'CONS'},
    {'name': 'KO', 'sector': 'CONS'},
    {'name': 'MCD', 'sector': 'CONS'},
    {'name': 'XOM', 'sector': 'ENERGY'},
    {'name': 'CVX', 'sector': 'ENERGY'},
    {'name': 'BP', 'sector': 'ENERGY'},
    # Add more stocks as needed
]

def create_stock_table(conn):
    """Create the Stock table if it doesn't exist."""
    conn.execute('''
        CREATE TABLE IF NOT EXISTS Stock (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            sector TEXT,
            price REAL,
            volatility REAL,
            growth_rate REAL,
            market_trend_influence REAL,
            company_performance REAL
        )
    ''')
    conn.commit()

def seed_stocks(conn):
    """Seed stocks into the Stock table."""
    for stock_info in STOCKS:
        sector = stock_info['sector']
        volatility_range = SECTORS[sector]['volatility']
        growth_rate_range = SECTORS[sector]['growth_rate']
        
        # Randomly assign stock-specific volatility and growth rate within sector range
        volatility = round(random.uniform(*volatility_range), 2)
        growth_rate = round(random.uniform(*growth_rate_range), 2)
        
        # Additional factors like sentiment impact and market trend sensitivity
        market_trend_influence = round(random.uniform(0.01, 0.05), 2)
        company_performance = round(random.uniform(0.8, 1.2), 2)
        price = round(random.uniform(50, 200), 2)  # Random starting price
        
        try:
            conn.execute('''
                INSERT INTO Stock (name, sector, price, volatility, growth_rate, market_trend_influence, company_performance)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (stock_info['name'], sector, price, volatility, growth_rate, market_trend_influence, company_performance))
            print(f"Created stock: {stock_info['name']} in sector {sector} with volatility {volatility}")
        except sqlite3.IntegrityError:
            print(f"Stock {stock_info['name']} already exists.")

    conn.commit()

if __name__ == '__main__':
    # Connect to the SQLite database (or create it if it doesn't exist)
    conn = sqlite3.connect('./db.sqlite3')  # Path to your SQLite database file
    create_stock_table(conn)
    seed_stocks(conn)
    conn.close()
