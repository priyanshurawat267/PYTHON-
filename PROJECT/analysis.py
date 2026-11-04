import numpy as np


def get_highest_price(df):
    return df["close"].max()


def get_lowest_price(df):
    return df["close"].min()


def get_average_price(df):
    return df["close"].mean()


def get_current_price(df):
    return df["close"].iloc[-1]


def get_price_range(df):
    return get_highest_price(df) - get_lowest_price(df)


def calculate_return(df):

    first_price = df["close"].iloc[0]
    last_price = df["close"].iloc[-1]

    return ((last_price - first_price) / first_price) * 100


def calculate_daily_return(df):

    df = df.copy()

    df["return"] = df["close"].pct_change() * 100

    return df


def calculate_volatility(df):

    df = calculate_daily_return(df)

    return np.std(
        df["return"].dropna()
    )


def calculate_moving_average(df, days=20):

    df = df.copy()

    df[f"MA{days}"] = (
        df["close"]
        .rolling(days)
        .mean()
    )

    return df


def analyze_stock(df):

    return {
        "current": get_current_price(df),
        "highest": get_highest_price(df),
        "lowest": get_lowest_price(df),
        "average": get_average_price(df),
        "range": get_price_range(df),
        "return": calculate_return(df),
        "volatility": calculate_volatility(df)
    }