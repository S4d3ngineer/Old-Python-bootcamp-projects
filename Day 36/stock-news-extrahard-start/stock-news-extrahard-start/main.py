import requests
import datetime
from twilio.rest import Client

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

today = datetime.date.today()
articles_list = []


# --------------------------------------------- API endpoints & keys ------------------------------------------------ #

# Provide the following
# ACCOUNT_SID = 
# AUTH_TOKEN = 

# ALPHAVANTAGE_KEY =
# ALPHAVANTAGE_ENDPOINT = 

# NEWSAPI_KEY = 
# NEWSAPI_ENDPOINT = 

# ----------------------------------------- Getting stock price change ---------------------------------------------- #

alpha_parameters = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "apikey": ALPHAVANTAGE_KEY
}

with requests.get(ALPHAVANTAGE_ENDPOINT, alpha_parameters) as r:
    r.raise_for_status()
    stock_data = r.json()

try:
    open_equity = float(stock_data["Time Series (Daily)"][f"{today}"]["1. open"])
    close_equity = float(stock_data["Time Series (Daily)"][f"{today}"]["4. close"])
except KeyError:
    open_equity = float(stock_data["Time Series (Daily)"][f"{today - datetime.timedelta(days=1)}"]["1. open"])
    close_equity = float(stock_data["Time Series (Daily)"][f"{today - datetime.timedelta(days=1)}"]["4. close"])


price_change = (open_equity - close_equity) / open_equity * 100
price_change_rounded = round(price_change, 2)


# ----------------------------------------- Getting news for given date --------------------------------------------- #


def get_news():
    global articles_list
    news_parameters = {
        "q": COMPANY_NAME,
        "apiKey": NEWSAPI_KEY,
        "sortBy": "publishedAt"
    }

    with requests.get(NEWSAPI_ENDPOINT, news_parameters) as r:
        r.raise_for_status()
        news_data = r.json()
        articles_list = news_data["articles"][0:3]

# ------------------------------------------------- Sending SMS ----------------------------------------------------- #


def send_sms(change, articles):
    client = Client(ACCOUNT_SID, AUTH_TOKEN)
    for n in range(3):
        message = client.messages \
            .create(
            body=f"""
            TSLA: {change}
            Headline:  {articles[n]["title"]}
            Brief: {articles[n]["description"]}
            """,
            from_='+17655629670',
            to='+48691029592',
        )

        print(message.status)

# ------------------------------------------------- if statement ---------------------------------------------------- #


# TODO: change percentage values back to 5!
if price_change_rounded >= 1:
    price_change_str = f"🔺{price_change_rounded}%"
    get_news()
    send_sms(price_change_str, articles_list)
elif price_change_rounded <= 1:
    price_change_str = f"🔻{price_change_rounded}%"
    get_news()
    send_sms(price_change_str, articles_list)
print(articles_list[0])

## STEP 1: Use https://www.alphavantage.co
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").

## STEP 2: Use https://newsapi.org
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME. 

## STEP 3: Use https://www.twilio.com
# Send a seperate message with the percentage change and each article's title and description to your phone number. 


#Optional: Format the SMS message like this:



