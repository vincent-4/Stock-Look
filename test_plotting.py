from main import plot_stock_price

ticker = 'AAPL'
image_path = plot_stock_price(ticker)
print(f"Plot saved at {image_path}")
