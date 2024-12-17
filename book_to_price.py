import yfinance as yf

# Fetch data for SOXL
ticker = "TSLA"
stock = yf.Ticker(ticker)

# Fetch market data
current_price = stock.history(period="1d")['Close'].iloc[-1]
info = stock.info

# Check if 'bookValue' exists
book_value = info.get('bookValue', None)
shares_outstanding = info.get('sharesOutstanding', None)

if book_value and shares_outstanding:
    # Calculate Market Cap and Book-to-Market Ratio
    market_value = current_price * shares_outstanding
    book_to_market_ratio = (market_value / shares_outstanding) / book_value

    # Print results
    print(f"Stock: {ticker}")
    print(f"Current Price: ${current_price:.2f}")
    print(f"Book Value Per Share: ${book_value:.2f}")
    print(f"Market Value Per Share: ${market_value / shares_outstanding:.2f}")
    print(f"Book-to-Market Ratio: {book_to_market_ratio:.4f}")
else:
    print("Book value or shares outstanding data not available for this ticker.")

# The book-to-market ratio compares a company’s net asset value or book value to its current or market value.
# If the company’s market value is trading higher than its book value per share, it is considered to be overvalued. 
# If the book value is higher than the market value, the company is considered to be undervalued.
    
print("\n")
if (book_to_market_ratio > 3):
    print("BTM ratio >1 shows company is undervalued. Trading at a much lower price.")
elif (book_to_market_ratio < 0):
    print("BTM ratio overvalued.")
else:
    print("Normal")