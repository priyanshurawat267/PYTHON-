
import requests
import pandas as pd
from datetime import datetime
from zoneinfo import ZoneInfo


BASE_URL = "https://query1.finance.yahoo.com/v8/finance/chart/{}"
HEADERS = {
    "User-Agent": "Mozilla/5.0"
}


def get_stock_data(symbol, interval="1m", period="1d"):
    """
    Fetch historical/intraday OHLCV stock data.

    interval: 1m, 5m, 15m, 1d etc.
    period: 1d, 5d, 1mo, 3mo, 1y etc.
    """

    symbol = symbol.strip().upper()

    if not symbol:
        raise ValueError("Stock symbol empty nahi ho sakta.")

    params = {
        "range": period,
        "interval": interval
    }

    try:
        response = requests.get(
            BASE_URL.format(symbol),
            params=params,
            headers=HEADERS,
            timeout=15
        )
        response.raise_for_status()
        payload = response.json()

        chart = payload.get("chart", {})
        results = chart.get("result")

        if not results:
            error = chart.get("error")
            message = error.get("description", "Data nahi mila.") if error else "Data nahi mila."
            print(f"{symbol}: {message}")
            return None

        result = results[0]
        timestamps = result.get("timestamp", [])
        quotes = result.get("indicators", {}).get("quote", [])

        if not timestamps or not quotes:
            return None

        quote = quotes[0]
        length = len(timestamps)

        df = pd.DataFrame({
            "date": pd.to_datetime(
                timestamps, unit="s", utc=True
            ).tz_convert("Asia/Kolkata").tz_localize(None),
            "open": quote.get("open", [])[:length],
            "high": quote.get("high", [])[:length],
            "low": quote.get("low", [])[:length],
            "close": quote.get("close", [])[:length],
            "volume": quote.get("volume", [])[:length]
        })

        df.dropna(
            subset=["open", "high", "low", "close"],
            inplace=True
        )

        df.sort_values("date", inplace=True)
        df.drop_duplicates(subset=["date"], keep="last", inplace=True)
        df.reset_index(drop=True, inplace=True)

        return df if not df.empty else None

    except requests.RequestException as error:
        print(f"Network/API error for {symbol}: {error}")
        return None
    except (ValueError, KeyError, IndexError, TypeError) as error:
        print(f"Data parsing error for {symbol}: {error}")
        return None


def get_live_stock_data(symbol):
    """
    Latest available price, candle high/low and data timestamp.
    """
    df = get_stock_data(
        symbol,
        interval="1m",
        period="1d"
    )

    if df is None or df.empty:
        return None

    latest = df.iloc[-1]

    return {
        "symbol": symbol.upper(),
        "price": float(latest["close"]),
        "high": float(latest["high"]),
        "low": float(latest["low"]),
        "volume": int(latest["volume"]),
        "timestamp": latest["date"],
        "data_fetched_at": datetime.now(
            ZoneInfo("Asia/Kolkata")
        ).strftime("%Y-%m-%d %H:%M:%S")
    }


def detect_price_change(symbol, previous_price=None):
    """
    Compare latest available price with previous fetched price.
    """
    live = get_live_stock_data(symbol)

    if live is None:
        return None

    current_price = live["price"]

    if previous_price is None:
        live["change"] = None
        live["change_percent"] = None
        live["direction"] = "FIRST FETCH"
    else:
        change = current_price - previous_price

        live["change"] = round(change, 4)
        live["change_percent"] = (
            round((change / previous_price) * 100, 4)
            if previous_price != 0 else None
        )

        if change > 0:
            live["direction"] = "UP"
        elif change < 0:
            live["direction"] = "DOWN"
        else:
            live["direction"] = "UNCHANGED"

    return live
