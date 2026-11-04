
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd


# 1. Candlestick Chart
def candlestick_chart(df, symbol):
    fig, ax = plt.subplots(figsize=(14, 6))

    dates = mdates.date2num(
        pd.to_datetime(df["date"]).dt.to_pydatetime()
    )

    for i in range(len(df)):
        open_price = df["open"].iloc[i]
        high_price = df["high"].iloc[i]
        low_price = df["low"].iloc[i]
        close_price = df["close"].iloc[i]

        color = "green" if close_price >= open_price else "red"

        # High-low line
        ax.plot(
            [dates[i], dates[i]],
            [low_price, high_price],
            color=color
        )

        # Candle body
        bottom = min(open_price, close_price)
        height = abs(close_price - open_price)

        if height == 0:
            height = 0.01

        ax.bar(
            dates[i],
            height,
            bottom=bottom,
            width=0.6,
            color=color
        )

    ax.set_title(f"{symbol} Candlestick Chart")
    ax.set_xlabel("Date")
    ax.set_ylabel("Price")
    ax.xaxis_date()

    ax.xaxis.set_major_formatter(
        mdates.DateFormatter("%b %Y")
    )

    ax.grid(True, alpha=0.3)
    plt.xticks(rotation=45)
    plt.tight_layout()

    return fig


# 2. Volume Chart
def volume_chart(df):
    fig, ax = plt.subplots(figsize=(14, 4))

    dates = pd.to_datetime(df["date"])

    ax.bar(dates, df["volume"], color="steelblue")

    ax.set_title("Trading Volume")
    ax.set_xlabel("Date")
    ax.set_ylabel("Volume")
    ax.grid(True, alpha=0.3)

    plt.xticks(rotation=45)
    plt.tight_layout()

    return fig


# 3. Combined Candlestick + Volume Chart
def show_candlestick_volume_chart(df, symbol):
    fig, (ax1, ax2) = plt.subplots(
        2,
        1,
        figsize=(14, 8),
        sharex=True,
        gridspec_kw={"height_ratios": [3, 1]}
    )

    dates = mdates.date2num(
        pd.to_datetime(df["date"]).dt.to_pydatetime()
    )

    # Candlestick chart
    for i in range(len(df)):
        open_price = df["open"].iloc[i]
        high_price = df["high"].iloc[i]
        low_price = df["low"].iloc[i]
        close_price = df["close"].iloc[i]

        color = "green" if close_price >= open_price else "red"

        # High-low line
        ax1.plot(
            [dates[i], dates[i]],
            [low_price, high_price],
            color=color,
            linewidth=1
        )

        # Candle body
        bottom = min(open_price, close_price)
        height = abs(close_price - open_price)

        if height == 0:
            height = 0.01

        ax1.bar(
            dates[i],
            height,
            bottom=bottom,
            width=0.6,
            color=color
        )

    ax1.set_title(f"{symbol} Candlestick + Volume Chart")
    ax1.set_ylabel("Price")
    ax1.grid(True, alpha=0.3)

    # Volume bars: green for up days, red for down days
    volume_colors = [
        "green" if df["close"].iloc[i] >= df["open"].iloc[i]
        else "red"
        for i in range(len(df))
    ]

    ax2.bar(
        dates,
        df["volume"],
        color=volume_colors,
        width=0.6
    )

    ax2.set_xlabel("Date")
    ax2.set_ylabel("Volume")
    ax2.set_title("Trading Volume")
    ax2.grid(True, alpha=0.3)

    ax2.xaxis_date()
    ax2.xaxis.set_major_formatter(
        mdates.DateFormatter("%b %Y")
    )

    plt.xticks(rotation=45)
    plt.tight_layout()

    return fig


# 4. Calculate Technical Indicators
def calculate_indicators(df):
    df = df.copy()

    if "close" not in df.columns:
        raise ValueError("DataFrame mein 'close' column nahi hai.")

    close = pd.to_numeric(df["close"], errors="coerce")

    # RSI (14 periods)
    delta = close.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = gain.ewm(
        alpha=1 / 14,
        min_periods=14,
        adjust=False
    ).mean()

    avg_loss = loss.ewm(
        alpha=1 / 14,
        min_periods=14,
        adjust=False
    ).mean()

    rs = avg_gain / avg_loss
    df["RSI"] = 100 - (100 / (1 + rs))

    df.loc[
        (avg_loss == 0) & (avg_gain > 0), "RSI"
    ] = 100

    df.loc[
        (avg_gain == 0) & (avg_loss == 0), "RSI"
    ] = 50

    # MACD (12, 26, 9)
    ema12 = close.ewm(span=12, adjust=False).mean()
    ema26 = close.ewm(span=26, adjust=False).mean()

    df["MACD"] = ema12 - ema26

    df["MACD_Signal"] = df["MACD"].ewm(
        span=9,
        adjust=False
    ).mean()

    df["MACD_Histogram"] = (
        df["MACD"] - df["MACD_Signal"]
    )

    # Bollinger Bands (20 periods)
    df["BB_Middle"] = close.rolling(20).mean()
    std = close.rolling(20).std()

    df["BB_Upper"] = df["BB_Middle"] + (2 * std)
    df["BB_Lower"] = df["BB_Middle"] - (2 * std)

    return df


# 5. Compare Two Stocks
def compare_stocks(df1, df2, symbol1, symbol2):
    fig, ax = plt.subplots(figsize=(14, 6))

    ax.plot(
        df1["date"],
        df1["close"],
        label=symbol1
    )

    ax.plot(
        df2["date"],
        df2["close"],
        label=symbol2
    )

    ax.set_title("Stock Price Comparison")
    ax.set_xlabel("Date")
    ax.set_ylabel("Closing Price")
    ax.legend()
    ax.grid(True, alpha=0.3)

    plt.xticks(rotation=45)
    plt.tight_layout()

    return fig


# Function aliases for compatibility
show_candlestick_chart = candlestick_chart
