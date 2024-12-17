import markdown

'''
The Five-Factor Asset Pricing Model is an extension of the widely used Capital Asset Pricing Model (CAPM) 
and the Fama-French Three-Factor Model. It was introduced by Eugene Fama and Kenneth French in 2015.
The model aims to explain stock returns by incorporating multiple factors beyond just market risk, accounting 
for variables such as size, value, profitability, and investment patterns. These factors have been empirically 
shown to better explain asset returns compared to the single-market-factor model of CAPM.
'''

# Link here
# https://www.sciencedirect.com/science/article/abs/pii/S0304405X14002323

# Shown as follows:

import yfinance as yf
import pandas as pd
import statsmodels.api as sm

# Download Fama-French five-factor data from Ken French's library (CSV file or API)
url = "https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html"
ff_data = pd.read_csv(url, skiprows=3, index_col=0)
ff_data.index = pd.to_datetime(ff_data.index, format='%Y%m')

# Get stock data for a specific ticker (SOXL)
ticker = "SOXL"
stock_data = yf.download(ticker, start="2010-01-01", end="2024-01-01")

# Calculate the excess return for the stock
stock_data['Excess_Return'] = stock_data['Adj Close'].pct_change() - ff_data['RF'] / 100

# Merge the stock data with the Fama-French factors
ff_data = ff_data.loc[stock_data.index]
data = pd.merge(stock_data, ff_data, left_index=True, right_index=True)

# Prepare the factors and dependent variable
X = data[['MKT', 'SMB', 'HML', 'RMW', 'CMA']]
X = sm.add_constant(X)  # Add a constant term for the intercept
y = data['Excess_Return']

# Perform regression
model = sm.OLS(y, X).fit()

# Print the results
print(model.summary())


