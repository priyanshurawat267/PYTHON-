from visualization import show_candlestick_volume_chart
from visualization import calculate_indicators
from api import get_stock_data
from analysis import analyze_stock
from visualization import (
    candlestick_chart,
    volume_chart,
    calculate_indicators
)
import os


symbols_input = input(
    "Enter stock symbols separated by comma: "
)

symbols = [
    symbol.strip().upper()
    for symbol in symbols_input.split(",")
]

stock_data = {}


for symbol in symbols:

    print(f"\nFetching {symbol}...")

    data = get_stock_data(symbol)

    if data is not None:
        data = calculate_indicators(data)
        print("RSI:", data["RSI"].iloc[-1])
        print("MACD:", data["MACD"].iloc[-1])
        print("MACD Signal:", data["MACD_Signal"].iloc[-1])
        print("Bollinger Upper:", data["BB_Upper"].iloc[-1])
        print("Bollinger Lower:", data["BB_Lower"].iloc[-1])

        stock_data[symbol] = data

        result = analyze_stock(data)

        print(f"\n===== {symbol} =====")
        print(f"Highest: ${result['highest']:.2f}")
        print(f"Lowest: ${result['lowest']:.2f}")
        print(f"Average: ${result['average']:.2f}")
        print(f"Return: {result['return']:.2f}%")
        print(f"Volatility: {result['volatility']:.2f}%")

        os.makedirs("data", exist_ok=True)

        filename = f"data/{symbol}_stock_data.csv"

        data.to_csv(
            filename,
            index=False
        )

        print(f"Saved: {filename}")


if len(stock_data) > 0:

    first_symbol = list(stock_data.keys())[0]

    candlestick_chart(
    stock_data[first_symbol],
    first_symbol
)
else:

    print("No stock data available.")