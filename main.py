import requests
from datetime import datetime
from twilio.rest import Client
import os

account_sid = os.getenv("account_sid")
auth_token = os.getenv("auth_token")

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
TWILIO_PHONE = os.getenv("twilio_phone")
TO_PHONE = os.getenv("to_phone")

alpha_api = os.getenv("alpha_api")
alpha_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "apikey": alpha_api
}
news_api = os.getenv("news_api")
news_params = {
    "q": STOCK,
    "from": datetime.now().date().isoformat(),
    "sortBy": "popularity",
    "apiKey": news_api
}

response = requests.get("https://www.alphavantage.co/query", params=alpha_params)
response.raise_for_status()

data = response.json()["Time Series (Daily)"]
data_list = [value for (key, value) in data.items()]
yest_stock_price = data_list[0]["4. close"]
yest2_stock_price = data_list[1]["4. close"]
#########################################################################################################
stock_diff = abs(float(yest_stock_price) - float(yest2_stock_price))
diff_percent = round(((stock_diff / float(yest_stock_price)) * 100), 2)
# print(round(diff_percent, 2))
if diff_percent >= 4:
    print("Get News")

    response2 = requests.get("https://newsapi.org/v2/everything", params=news_params)
    response2.raise_for_status()
    data2 = response2.json()["articles"]
    # for i in range (0, 3):
    #     print(data2[i]["description"])
    three_articles = data2[:3]

    client = Client(account_sid, auth_token)
    for i in range(0, 3):
        if float(yest2_stock_price) - float(yest_stock_price) > 0:
            print(f"""{STOCK}: 🔺{diff_percent}%\nHeadline: {three_articles[i]["title"]}\nBrief: {three_articles[i]["description"]}""")
            message = client.messages.create(to=TO_PHONE, from_=TWILIO_PHONE, body=f"""{STOCK}: 🔺{diff_percent}\nHeadline: {three_articles[i]["title"]}\nBrief: {three_articles[i]["description"]}""")
        else:
            print(f"""{STOCK}: 🔻{diff_percent}%\nHeadline: {three_articles[i]["title"]}\nBrief: {three_articles[i]["description"]}""")
            message = client.messages.create(to=TO_PHONE, from_=TWILIO_PHONE, body=f"""{STOCK}: 🔻{diff_percent}\nHeadline: {three_articles[i]["title"]}\nBrief: {three_articles[i]["description"]}""")

        print(message.status)



