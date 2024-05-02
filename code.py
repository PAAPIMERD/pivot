#must includes all the import and downloads
import time
from kite_trade import *
from datetime import datetime
import neo_api_client
from neo_api_client import NeoAPI
enctoken = "5BBCmULwwFHPAU8/2/xdN+VknZIeiOsRBzNUrzDdINetraZInF7LrdteAemZ1FK7q6bNRokCcx51EgH5MJI282vjvld7OA/IqFPTxH23xe02O6KSoDHSDw=="
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
  
def fib_pivot_gen(prev_high,prev_low,prev_close):
  global PP,R1,S1,R2,S2,R3,S3
  PP = (prev_high+prev_low+prev_close)/3
  R1 =PP + 0.382 * (prev_high - prev_low)
  S1 = PP - 0.382 * (prev_high - prev_low)
  R2 = PP + 0.618 * (prev_high - prev_low)
  S2 = PP - 0.618 * (prev_high - prev_low)
  R3 = PP + (prev_high - prev_low)
  S3 = PP - (prev_high - prev_low)
  return PP,R1,S1,R2,S2,R3,S3


fib_pivot_gen(286.35,281.45,282.85)





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




def range_finder(curr_price):
  curr_price = float(curr_price)
  global PP,R1,S1,R2,S2,R3,S3
  
  if curr_price<R3 and curr_price>R2:
    return 3
  if curr_price<R2 and curr_price>R1:
    return 2
  if curr_price<R1 and curr_price>PP:
    return 1
  if curr_price<PP and curr_price>S1:
    return 0
  if curr_price<S1 and curr_price>S2:
    return -1
  if curr_price<S2 and curr_price>S3:
    return -2



def next_green_pivot(curr_price):
    global PP, R1, S1, R2, S2, R3, S3
    
    pivot_levels = [PP, R1, S1, R2, S2, R3, S3]
    closest_greater = None
    
    for level in pivot_levels:
        if level > curr_price:
            if closest_greater is None or level < closest_greater:
                closest_greater = level
    
    return closest_greater



direction = ""   #can have values as red or green only
tracker = [0]
initial_balance = ""

def start(symbol):
  curr_price = price_fetcher(symbol)
  global tracker,direction
  curr_piv = range_finder(curr_price)
  tracker.append(curr_piv)
  if len(tracker) >= 40:
    tracker.pop(0)
  while True:
    curr_price = price_fetcher(symbol)
    now_piv = range_finder(curr_price)
    tracker.append(now_piv)
    if tracker[-1] > tracker[-2]:
      stage = tracker[-1]
      target = next_green_pivot(curr_price)
      if target == None:
        break
        time.sleep(36000)
      dec_price = price_fetcher(symbol)
      stop_loss = dec_price - (0.12/100)*dec_price
      buy()
      #call the buy function here at self to execute the buy order at the current market price
      return sl_or_target(symbol,target,stop_loss,now_piv)


def sl_or_target(symbol,target,stop_loss,now_piv):
  while True:
    curr_price = price_fetcher(symbol)
    if curr_price <= stop_loss:
      print("stoploss has been breached")
      #call to selling function
      sell()
      return start(symbol)
    if curr_price >= target:
      #call to sell the function
      time.sleep(1)
      now_range = range_finder(curr_price)
      if now_range == now_piv+1:
        curr_price = price_fetcher(symbol)
        #code to buy the instruement at the cmp
        buy()
        target = next_green_pivot(curr_price)
        if target == None:
          break
          time.sleep(36000)
        stop_loss = curr_price - (0.12/100)*curr_price
        return sl_or_target(symbol,target,stop_loss,now_range)
    else:
      return start(symbol)



def check_time():
    while True:
        current_time = datetime.now()
        current_hour = current_time.hour+5
        current_minute = current_time.minute+30
        if current_hour == 9 and current_minute == 15:
            start()
            break
        time.sleep(1)  # Check every minute


start("ONGC")
