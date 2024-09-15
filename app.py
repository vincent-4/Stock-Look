import yfinance as yf
import matplotlib.pyplot as plt
import requests
import subprocess
from textblob import TextBlob
from flask import Flask, render_template, request
import os

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        ticker = request.form['ticker']
        results = get_stock_info(ticker)
        return render_template('results.html', results=results)
    return render_template('index.html')

def get_news_sentiment(ticker):
    url = f'https://newsapi.org/v2/everything?q={ticker}&apiKey=20e82b1b7a6040ce952ab5380c075898'
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad responses
        articles = response.json().get('articles', [])
        
        sentiments = []
        headlines = []
        for article in articles[:5]:  # Analyze top 5 articles
            text = article['title'] + ' ' + article['description']
            sentiment = TextBlob(text).sentiment.polarity
            sentiments.append(sentiment)
            headlines.append(article['title'])
        
        avg_sentiment = sum(sentiments) / len(sentiments) if sentiments else 0
        
        return {
            'average_sentiment': avg_sentiment,
            'article_count': len(sentiments),
            'headlines': headlines
        }
    except requests.RequestException as e:
        print(f"Error fetching news data: {e}")
        return None


def get_stock_info(ticker):
    commands = [
        f"get_stock_price {ticker}",
        f"calculate_SMA {ticker} 20",
        f"calculate_EMA {ticker} 20",
        f"calculate_RSI {ticker}",
        f"calculate_MACD {ticker}",
        f"plot_stock_price {ticker}",
    ]
    results = []

    for command in commands:
        process = subprocess.Popen(["python", "main.py"], 
        stdout=subprocess.PIPE, stdin=subprocess.PIPE, 
        stderr=subprocess.PIPE, text=True)
        output, _ = process.communicate(input=command)
        try:
            # Try to convert the output to float and round it
            results.append(round(float(output.strip()), 2))
        except ValueError:
            # If conversion fails, append the original string
            results.append(output.strip())

    return results

if __name__ == '__main__':
    app.run(debug=True)

