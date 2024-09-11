from django.apps import AppConfig
import threading
from .utils import simulate_market

class TradeappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'tradeapp'
    
    def ready(self):
        threading.Thread(target=simulate_market).start()
