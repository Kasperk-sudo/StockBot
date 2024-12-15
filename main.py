import requests
from twilio.rest import Client
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv



from dotenv import load_dotenv
import os

# Load environment variables from the .env file
load_dotenv("project")

# Access the variables
api_key = os.getenv("API_KEY") ## https://www.alphavantage.co/
news_api_key = os.getenv("NEWS_API_KEY") ## https://newsapi.org/
acc_sid = os.getenv("TWILIO_ACC_SID") ##  https://www.twilio.com/en-us
auth_token = os.getenv("TWILIO_AUTH_TOKEN") ## https://www.twilio.com/en-us



client = Client(acc_sid, auth_token)
STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={STOCK_NAME}&apikey={api_key}"
NEWS_ENDPOINT = f"https://newsapi.org/v2/everything?q={STOCK_NAME}&apikey={news_api_key}"


params={
    "q": COMPANY_NAME,
    "apiKey": api_key
}



response = requests.get(STOCK_ENDPOINT, params=params)
response.raise_for_status()
data = response.json()

response2 = requests.get(NEWS_ENDPOINT)
response2.raise_for_status()
data2 = response2.json()
articles = data2.get("articles", [])
first_three_articles = articles[:3]

today = datetime.now()
yesterday = (today - timedelta(days=1)).strftime("%Y-%m-%d")
day_before_yesterday = (today - timedelta(days=2)).strftime("%Y-%m-%d")

stock_data = float(data['Time Series (Daily)'][yesterday]['4. close'])
stock_data2 = float(data['Time Series (Daily)'][day_before_yesterday]['4. close'])



def percent(a, b):

    return abs(((b - a) * 100) / a)

change_percentage = percent(stock_data, stock_data2)
formatted_num = "%.2f" % change_percentage
if change_percentage > 5:
    print("Significant stock price change. Fetching news...")
    response2 = requests.get(NEWS_ENDPOINT)
    response2.raise_for_status()
    data2 = response2.json()

    # Get first three articles
    articles = data2.get("articles", [])
    first_three_articles = articles[:3]

    # Send Articles to WhatsApp
    for article in first_three_articles:
        title = article.get("title", "No title available")
        description = article.get("description", "No description available")
        url = article.get("url", "No URL available")

        message_body = f"TSLA 🔺{formatted_num}% News Update:\n\n*Title*: {title}\n*Description*: {description}\n*URL*: {url}"

        message = client.messages.create(
            body=message_body,
            from_="whatsapp:", ## get a whatsapp number from twilio https://www.twilio.com/en-us
            to="whatsapp:+" ## your phone number
        )
        print(f"Message sent: {message.sid}")
else:
    print("Stock price change is not significant.")

