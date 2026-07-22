import yfinance as yf
ticker = "XOM"
xom = yf.download(tickers = ticker, start = "2023-01-01", end = "2026-07-01", interval = "1d")
print(xom)

