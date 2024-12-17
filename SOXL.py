import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import os

def fetch_and_update_data(ticker="SOXL", filename="soxl_data.csv"):
    """
    Fetch new stock data and update the existing data file.
    """
    if os.path.exists(filename):
        try:
            # Try reading the file with 'Date' as index
            existing_data = pd.read_csv(filename, index_col="Date", parse_dates=True)
            if existing_data.empty:
                print("Existing file is empty. Refetching full data...")
                raise ValueError("Empty file")
            
            last_date = existing_data.index[-1]  # Get the last date
            print(f"Last date in the file: {last_date}")

            # Fetch new data starting from the next day
            new_data = yf.download(ticker, start=last_date + pd.Timedelta(days=1))
        except (ValueError, KeyError, pd.errors.EmptyDataError):
            # If the file is corrupt or missing headers, fetch fresh data
            print("File is corrupt or missing headers. Fetching fresh data...")
            new_data = yf.download(ticker, period="1y")
            existing_data = pd.DataFrame()  # Set as empty DataFrame
    else:
        print("No existing data file found. Fetching new data...")
        new_data = yf.download(ticker, period="1y")
        existing_data = pd.DataFrame()

    # Combine and save the data
    combined_data = pd.concat([existing_data, new_data])
    combined_data = combined_data[~combined_data.index.duplicated(keep='last')]
    combined_data.to_csv(filename)
    print("Data updated successfully!")
    return combined_data

def plot_stock_data(data, start_date=None, end_date=None):
    """
    Plot stock data with optional filtering by date range.
    """
    if start_date or end_date:
        data = data.loc[start_date:end_date]

    plt.figure(figsize=(12, 6))
    plt.plot(data.index, data["Open"], label="Open", alpha=0.7)
    plt.plot(data.index, data["Close"], label="Close", alpha=0.7)
    plt.plot(data.index, data["High"], label="High", alpha=0.7)
    plt.plot(data.index, data["Low"], label="Low", alpha=0.7)

    plt.title("SOXL Stock Prices")
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.legend()
    plt.grid()
    plt.show()

# Update or fetch data
stock_data = fetch_and_update_data()

# Plot the updated data
plot_stock_data(stock_data)

# Optional: Filter data interactively
start_date = input("Enter start date (YYYY-MM-DD) or leave blank: ")
end_date = input("Enter end date (YYYY-MM-DD) or leave blank: ")
plot_stock_data(stock_data, start_date=start_date if start_date else None, end_date=end_date if end_date else None)


def plot_stock_data(data, start_date=None, end_date=None):
    """
    Plot stock data with optional filtering by date range.
    """
    if start_date or end_date:
        data = data.loc[start_date:end_date]

    plt.figure(figsize=(12, 6))
    plt.plot(data.index, data["Open"], label="Open", alpha=0.7)
    plt.plot(data.index, data["Close"], label="Close", alpha=0.7)
    plt.plot(data.index, data["High"], label="High", alpha=0.7)
    plt.plot(data.index, data["Low"], label="Low", alpha=0.7)

    plt.title("SOXL Stock Prices")
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.legend()
    plt.grid()
    plt.show()

# Update or fetch data
stock_data = fetch_and_update_data()

# Plot the updated data
plot_stock_data(stock_data)

# Optional: Filter data interactively
start_date = input("Enter start date (YYYY-MM-DD) or leave blank: ")
end_date = input("Enter end date (YYYY-MM-DD) or leave blank: ")
plot_stock_data(stock_data, start_date=start_date if start_date else None, end_date=end_date if end_date else None)
