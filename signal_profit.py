import matplotlib.pyplot as plt

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
        elif current_signal == "Sell" and buy_price is not None:
            trade_pnl = current_price - buy_price
            data.at[date, "Trade_PnL"] = trade_pnl
            total_pnl += trade_pnl
            buy_price = None
    if buy_price is not None:
        last_price = float(data["Close"].iloc[-1])
        open_position_pnl = last_price - buy_price
        total_pnl += open_position_pnl

    return data, total_pnl

