from .models import Stock

def update_all_stock_sentiments():
    """Update sentiment and predictors for all stocks."""
    stocks = Stock.objects.all()
    for stock in stocks:
        stock.update_sentiment()