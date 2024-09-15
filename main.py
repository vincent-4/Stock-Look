import json
import re
import openai
import yfinance as yf
import matplotlib.pyplot as plt
import os
import flask

from dotenv import load_dotenv
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def get_stock_price(ticker):
    return str(yf.Ticker(ticker).history(period='1y').iloc[-1].Close)

def calculate_SMA(ticker, window):
    data = yf.Ticker(ticker).history(period='1y').Close
    return str(data.rolling(window=window).mean().iloc[-1])

def calculate_EMA(ticker, window):
    data = yf.Ticker(ticker).history(period='1y').Close
    return str(data.ewm(span=window, adjust=False).mean().iloc[-1])

def calculate_RSI(ticker):
    data = yf.Ticker(ticker).history(period='1y').Close
    delta = data.diff()
    up = delta.clip(lower=0)
    down = -1 * delta.clip(upper=0)
    ema_up = up.ewm(com=14 - 1, adjust=False).mean()
    ema_down = down.ewm(com=14 - 1, adjust=False).mean()
    rs = ema_up / ema_down
    return str(100 - (100 / (1 + rs)).iloc[-1])

def calculate_MACD(ticker):
    data = yf.Ticker(ticker).history(period='1y').Close
    short_EMA = data.ewm(span=12, adjust=False).mean()
    long_EMA = data.ewm(span=26, adjust=False).mean()
    MACD = short_EMA - long_EMA
    signal = MACD.ewm(span=9, adjust=False).mean()
    MACD_histogram = MACD - signal
    return f'{MACD.iloc[-1]}, {signal.iloc[-1]}, {MACD_histogram.iloc[-1]}'

def plot_stock_price(ticker):
    data = yf.Ticker(ticker).history(period='1y')[['Close']]
    data.reset_index(inplace=True)  # Reset the index to make 'Date' a column
    plt.figure(figsize=(10, 5))
    plt.plot(data['Date'], data['Close'])
    plt.title(f'{ticker} Stock Price Over Last Year')
    plt.xlabel('Date')
    plt.ylabel('Stock Price ($)')
    plt.grid(True)
    image_path = os.path.join("static", "stock.png")
    plt.savefig(image_path)
    plt.close()
    return image_path



def main():
    while True:
        user_input = input(' ')
        if user_input.lower() == 'exit':
            break
        elif user_input.startswith('get_stock_price'):
            parts = user_input.split(' ')
            if len(parts) == 2:
                ticker = parts[1]
                result = get_stock_price(ticker)
                print(result)
            else:
                print("Invalid input. Usage: get_stock_price <ticker>")
        elif user_input.startswith('calculate_SMA'):
            parts = user_input.split(' ')
            if len(parts) == 3:
                ticker = parts[1]
                window = int(parts[2])
                result = calculate_SMA(ticker, window)
                print(result)
            else:
                print("Invalid input. Usage: calculate_SMA <ticker> <window>")
        elif user_input.startswith('calculate_EMA'):
            parts = user_input.split(' ')
            if len(parts) == 3:
                ticker = parts[1]
                window = int(parts[2])
                result = calculate_EMA(ticker, window)
                print(result)
            else:
                print("Invalid input. Usage: calculate_EMA <ticker> <window>")
        elif user_input.startswith('calculate_RSI'):
            parts = user_input.split(' ')
            if len(parts) == 2:
                ticker = parts[1]
                result = calculate_RSI(ticker)
                print(result)
            else:
                print("Invalid input. Usage: calculate_RSI <ticker>")
        elif user_input.startswith('calculate_MACD'):
            parts = user_input.split(' ')
            if len(parts) == 2:
                ticker = parts[1]
                result = calculate_MACD(ticker)
                print(result)

        elif user_input.startswith('plot_stock_price'):
            parts = user_input.split(' ')
            if len(parts) == 2:
                ticker = parts[1]
                plot_stock_price(ticker)
                plt.savefig('stock.png')
            else:
                print("Invalid input. Usage: calculate_MACD <ticker>")
        else:
            print("Invalid command. Supported commands: get_stock_price, calculate_SMA, calculate_EMA, calculate_RSI, calculate_MACD, exit")

if __name__ == '__main__':
    main()
