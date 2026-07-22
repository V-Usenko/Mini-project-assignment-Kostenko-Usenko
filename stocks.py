import yfinance as yf
import matplotlib.pyplot as plt

ticker = "XOM"
xom = yf.download(tickers = ticker, start = "2023-01-01", end = "2026-07-01", interval = "1d")
print(xom)

xom["50-Day-MA"] = xom["Close"].rolling(window=50).mean()
xom["200-Day-MA"] = xom["Close"].rolling(window=200).mean()

clean_xom_close = xom[["Close", "50-Day-MA", "200-Day-MA"]].dropna()
print(clean_xom_close)

plt.figure(figsize = (13,7))
plt.plot(clean_xom_close["50-Day-MA"], label = "50-Day Moving Average", color = "blue")
plt.plot(clean_xom_close["200-Day-MA"], label = "200-Day Moving Average", color = "green")
plt.title("ExxonMobil(XOM) 50 and 200 Day Moving Average")
plt.xlabel("Date")
plt.ylabel("Price, $")
plt.legend()
plt.grid()
plt.show()


