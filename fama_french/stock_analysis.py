import pandas as pd
import yfinance as yf
import statsmodels.api as sm

# Function to fetch stock data
def fetch_stock_data(ticker, start_date, end_date):
    stock = yf.Ticker(ticker)
    stock_data = stock.history(start=start_date, end=end_date)['Close']
    return stock_data

# Function to load Fama-French 5-factor data
def load_fama_french_data(file_path):
    fama_french = pd.read_csv(file_path, skiprows=3)
    fama_french = fama_french.rename(columns=lambda x: x.strip())  # Clean column names
    fama_french['Date'] = pd.to_datetime(fama_french['Unnamed: 0'], format='%Y%m%d')
    fama_french = fama_french.drop(columns=['Unnamed: 0'])
    fama_french = fama_french.set_index('Date') / 100  # Convert percentages to decimals
    return fama_french

# Function to calculate stock returns
def calculate_stock_returns(stock_data):
    stock_returns = stock_data.pct_change().dropna()
    return stock_returns

# Function to merge stock returns and Fama-French factors
def merge_data(stock_returns, fama_french):
    merged_data = pd.concat([stock_returns, fama_french], axis=1).dropna()
    merged_data = merged_data.rename(columns={'Close': 'Stock_Returns'})
    return merged_data

# Function to run OLS regression for the five-factor model
def run_regression(merged_data):
    X = merged_data[['Mkt-RF', 'SMB', 'HML', 'RMW', 'CMA']]  # Fama-French factors
    y = merged_data['Stock_Returns'] - merged_data['RF']  # Excess return over risk-free rate
    
    # Add constant term for the intercept (alpha)
    X = sm.add_constant(X)

    # Run the OLS regression
    model = sm.OLS(y, X).fit()

    return model

# Main execution
if __name__ == "__main__":
    # Set the stock ticker and date range
    ticker = "TSLA"
    start_date = "2023-01-01"
    end_date = "2024-01-01"
    
    # Fetch stock data and calculate returns
    stock_data = fetch_stock_data(ticker, start_date, end_date)
    stock_returns = calculate_stock_returns(stock_data)
    
    # Load the Fama-French Five-Factor data
    file_path = 'fama_french/fama_french_data.csv'
    fama_french_data = load_fama_french_data(file_path)
    
    # Merge stock returns with Fama-French data
    combined_data = merge_data(stock_returns, fama_french_data)
    
    # Run the regression
    model = run_regression(combined_data)
    
    # Print the results
    print(model.summary())
