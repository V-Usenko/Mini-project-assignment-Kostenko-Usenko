import yfinance as yf
import matplotlib.pyplot as plt

ticker = "XOM"
xom = yf.download(tickers = ticker, start = "2023-01-01", end = "2026-07-01", interval = "1d")
xom.columns = xom.columns.get_level_values(0)
print("Історичні дані ExxonMobil:")
print(xom)

xom["50-Day-MA"] = xom["Close"].rolling(window=50).mean()
xom["200-Day-MA"] = xom["Close"].rolling(window=200).mean()

clean_xom_close = xom[["Close", "50-Day-MA", "200-Day-MA"]].dropna()
print("Ціна при закритті та ковзні середні за 50 і 200 днів:")
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


def add_trading_signals(data):
    data = data.copy()
    data["Signal"] = "Hold"
    previous_short_ma = data["50-Day-MA"].shift(1)
    previous_long_ma = data["200-Day-MA"].shift(1)
    buy_condition = ((data["50-Day-MA"] > data["200-Day-MA"])&(previous_short_ma <= previous_long_ma))
    sell_condition = ((data["50-Day-MA"] < data["200-Day-MA"])&(previous_short_ma >= previous_long_ma))
    data.loc[buy_condition, "Signal"] = "Buy"
    data.loc[sell_condition, "Signal"] = "Sell"

    return data

def calculate_pnl(data):
    data = data.copy()
    data["Trade_PnL"] = 0.0
    buy_price = None
    total_pnl = 0.0

    for date, row in data.iterrows():
        current_price = float(row["Close"])
        current_signal = row["Signal"]

        if current_signal == "Buy" and buy_price is None:
            buy_price = current_price
            print(f"Купівля, дата: {date.date()}, ціна: ${buy_price:.2f}")

        elif current_signal == "Sell" and buy_price is not None:
            trade_pnl = current_price - buy_price
            data.at[date, "Trade_PnL"] = trade_pnl
            total_pnl += trade_pnl
            print(f"Продаж, дата: {date.date()}, ціна: ${current_price:.2f}, P&L: ${trade_pnl:.2f}")
            buy_price = None

    if buy_price is not None:
        last_price = float(data["Close"].iloc[-1])
        open_position_pnl = last_price - buy_price
        total_pnl += open_position_pnl
        print(f"Відкрита позиція, остання ціна: ${last_price:.2f}, P&L: ${open_position_pnl:.2f}")

    return data, total_pnl


clean_xom_close = add_trading_signals(clean_xom_close)
clean_xom_close, total_pnl = calculate_pnl(clean_xom_close)
trades = clean_xom_close[clean_xom_close["Signal"] != "Hold"]

print("Торгові сигнали:")
print(trades[["Close", "50-Day-MA", "200-Day-MA", "Signal", "Trade_PnL"]])
print(f"Загальний P&L: ${total_pnl:.2f}")

buy = clean_xom_close[clean_xom_close["Signal"] == "Buy"]
sell = clean_xom_close[clean_xom_close["Signal"] == "Sell"]

plt.figure(figsize = (15,8))
plt.plot(clean_xom_close["50-Day-MA"], label = "50-Day Moving Average", color = "blue")
plt.plot(clean_xom_close["200-Day-MA"], label = "200-Day Moving Average", color = "green")
plt.plot(clean_xom_close["Close"], label = "Close price", color = "darkgrey")
plt.scatter(buy.index, buy["50-Day-MA"], label = "Buy", color = "green", marker = "^", s = 100)
plt.scatter(sell.index, sell["50-Day-MA"], label = "Sell", color = "red", marker = "v", s = 100)
plt.title("ExxonMobil(XOM) 50 and 200 Day Moving Average")
plt.xlabel("Date")
plt.ylabel("Price, $")
plt.legend()
plt.grid()
plt.show()

investment = 100000

buy_price = clean_xom_close[clean_xom_close["Signal"] == "Buy"]["Close"].iloc[0]
number_of_shares = investment / buy_price
number_of_shares = round(number_of_shares, 2)

total_profit = number_of_shares * total_pnl
final_suma = investment + total_profit
roi = (total_profit / investment) * 100
date = clean_xom_close[clean_xom_close["Signal"] == "Buy"].index[0]
print(f"Інвестувавши {investment}$ {date}, отримали б {number_of_shares} акцій, дохід {total_profit:.2f}$, загальний дохід {final_suma:.2f}$ та roi {roi:.2f}%")

