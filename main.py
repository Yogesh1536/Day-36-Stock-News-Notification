import requests
from twilio.rest import Client

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
STOCK_API_KEY = "1DE9****V19DZC1U"  # use your own stock api key
account_sid = "AC0a94f226912db29d1087ab9fe278634f"  # use your account id from twilio
auth_token = "2f1a87856d36637f11e3294*****5b72"  # use your own authentication token from twilio

stck_parameter = {
    "function": "TIME_SERIES_DAILY_ADJUSTED",
    "symbol": STOCK_NAME,
    "apikey": STOCK_API_KEY
}
response = requests.get(STOCK_ENDPOINT, params=stck_parameter)
response.raise_for_status()
stock_data = response.json()["Time Series (Daily)"]
data_list = [values for (keys, values) in stock_data.items()]
yesterday_data = data_list[0]
y_closing_price = float(yesterday_data["4. close"])

dby_data = data_list[1]
dby_close_price = float(dby_data["4. close"])
difference = y_closing_price - dby_close_price

up_down = None
if difference > 0:
    up_down = "🔺"
else:
    up_down = "🔻"

diff_percent = round(abs(difference / y_closing_price) * 100)

if abs(diff_percent) > 1:

    news_parameter = {
        "q": COMPANY_NAME,
        "apikey": "6b68e87ba8fd4cb******057f0baaad5"   # use your own news api key
    }
    news_response = requests.get(NEWS_ENDPOINT, params=news_parameter)
    news_response.raise_for_status()
    content = news_response.json()
    articles = content["articles"]
    recent_3 = articles[:3]
    formatted = [f"{STOCK_NAME}: {up_down}{diff_percent}% \nTitle:{article['title']}.\nBrief:{article['content']}" for
                 article in recent_3]

    client = Client(account_sid, auth_token)

    for article in formatted:
        message = client.messages.create(
            body=article,
            from_="+16206986017",  # use number that alerted from twilio for you
            to='+919080114615'  # use your verified mobile number in twilio
        )
