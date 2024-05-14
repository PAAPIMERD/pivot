#must includes all the import and downloads
import time
from kite_trade import *
from datetime import datetime
import neo_api_client
from neo_api_client import NeoAPI
enctoken = "2g5rlyFLveEkZwoo3/m7I9jI3XsUSfcV3uIv22/9uZcDtNfc6laFAaGFo8yKOJFayPpassobrp9oKAotEHM2K49D70hUbikGP8GzFic/voD0N6tWHriOIA=="
kite = KiteApp(enctoken=enctoken)
cons_key = "vvdHaGEFcURbb36F0DVJfDkW0CQa"
cons_sec = "DgTu4TNBTW6yLXb7nF08knjY_HUa"
mobile = "+916303008951"
paswd = "Avks@1234"
mpin = "271707"

client = NeoAPI(consumer_key=cons_key, consumer_secret=cons_sec, environment='prod',
                access_token=None, neo_fin_key=None)

client.login(mobilenumber=mobile, password=paswd)
client.session_2fa(OTP=mpin)

def buy():
  client.place_order(exchange_segment="nse_cm", product="MIS", price="", order_type="MKT", quantity="1", validity="DAY", trading_symbol="ONGC-EQ",
                       transaction_type="B", amo="NO", disclosed_quantity="0", market_protection="0", pf="N",
                       trigger_price="0", tag=None)
  
def sell():
  client.place_order(exchange_segment="nse_cm", product="MIS", price="", order_type="MKT", quantity="1", validity="DAY", trading_symbol="ONGC-EQ",
                       transaction_type="S", amo="NO", disclosed_quantity="0", market_protection="0", pf="N",
                       trigger_price="0", tag=None)
  






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
  print("buy order executed at ONGC-EQ" at the priceof ",price_fetcher("ONGC"))
  time.sleep(30)
  sell()
  print("buy order executed at ONGC-EQ" at the priceof ",price_fetcher("ONGC"))
