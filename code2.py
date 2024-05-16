#must includes all the import and downloads
import time
from kite_trade import *
from datetime import datetime

enctoken = "ZWHsDU+s/3hwSS1INwrfJ5qaLaCPEe6/O3HbHZTJ3/W2AQVif9F1WDfFh9qJDVdxuhEMqbjh8VCN0WpjihsNWc+YWfhiMoivdL95E2GlLu59Znm0b0QuyQ=="
kite = KiteApp(enctoken=enctoken)



def buy():
  order = kite.place_order(variety=kite.VARIETY_REGULAR,
                         exchange=kite.EXCHANGE_NSE,
                         tradingsymbol="ONGC",
                         transaction_type=kite.TRANSACTION_TYPE_BUY,
                         quantity=1,
                         product=kite.PRODUCT_MIS,
                         order_type=kite.ORDER_TYPE_MARKET,
                         price=None,
                         validity=None,
                         disclosed_quantity=None,
                         trigger_price=None,
                         squareoff=None,
                         stoploss=None,
                         trailing_stoploss=None,
                         tag="TradeViaPython")

def sell():
  order = kite.place_order(variety=kite.VARIETY_REGULAR,
                         exchange=kite.EXCHANGE_NSE,
                         tradingsymbol="ONGC",
                         transaction_type=kite.TRANSACTION_TYPE_SELL,
                         quantity=1,
                         product=kite.PRODUCT_MIS,
                         order_type=kite.ORDER_TYPE_MARKET,
                         price=None,
                         validity=None,
                         disclosed_quantity=None,
                         trigger_price=None,
                         squareoff=None,
                         stoploss=None,
                         trailing_stoploss=None,
                         tag="TradeViaPython")
  







def price_fetcher(symbol):
    start_time = time.time()  # Record the start time

    while True:
        try:
            # Attempt to fetch the price
            price = kite.ltp(["NSE:" + symbol])
            final_price = price["NSE:" + symbol]["last_price"]
            return final_price
        except KeyError as e:
            # Handle KeyError
            elapsed_time = time.time() - start_time
            if elapsed_time >= 60:
                # If 60 seconds have passed and price is still not fetched, raise an exception
                raise Exception("Failed to fetch price for symbol {} after 60 seconds".format(symbol))

            # Sleep for a short interval before retrying
            time.sleep(0.001)  # Retry every 0.001 seconds


while True:
  buy()
  print("buy order executed at ONGC-EQ at the price of ", price_fetcher("ONGC"))

  time.sleep(90)
  sell()
  print("sell order executed at ONGC-EQ at the price of ", price_fetcher("ONGC"))

