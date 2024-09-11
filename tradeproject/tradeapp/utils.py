from .models import Stock
import threading

def simulate_market():
    """Simulate the market by updating stock prices periodically."""
    stocks = Stock.objects.all()
    for stock in stocks:
        stock.update_price()

    threading.Timer(5.0, simulate_market).start()

