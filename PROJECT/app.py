
import streamlit as st
import pandas as pd

from api import get_stock_data
from analysis import (
    analyze_stock,
    calculate_moving_average
)
from visualization import (
    candlestick_chart,
    volume_chart
)


# =====================================
# PAGE SETTINGS
# =====================================

st.set_page_config(
    page_title="Stock Market Analyzer",
    page_icon="📈",
    layout="wide"
)


# =====================================
# LOGIN SYSTEM
# =====================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "email" not in st.session_state:
    st.session_state.email = ""

if "previous_prices" not in st.session_state:
    st.session_state.previous_prices = {}

if "last_symbol" not in st.session_state:
    st.session_state.last_symbol = ""


if not st.session_state.logged_in:

    st.title("📈 Stock Market Analyzer")
    st.write("Login to continue")

    email = st.text_input("Email")

    password = st.text_input(
        "Password",
        type="password"
    )

    if st.button("Login", type="primary"):

        if email.strip() and password:

            st.session_state.logged_in = True
            st.session_state.email = email.strip()

            st.rerun()

        else:
            st.error("Please enter email and password.")

    st.info(
        "Demo login: this checks only whether fields are filled. "
        "It does not authenticate a real account."
    )

    st.stop()


# =====================================
# MAIN APPLICATION
# =====================================

st.title("📈 Stock Market Analyzer")

st.write(
    f"Welcome, {st.session_state.email}"
)

st.caption(
    "Analyze historical stock data or monitor the latest "
    "available intraday prices."
)


# =====================================
# SIDEBAR SETTINGS
# =====================================

st.sidebar.header("Stock Settings")

symbol = st.sidebar.text_input(
    "Stock Symbol",
    value="AAPL"
).strip().upper()

mode = st.sidebar.radio(
    "Analysis Mode",
    [
        "Historical (1 Year)",
        "Live / Intraday"
    ]
)

ma_days = st.sidebar.number_input(
    "Moving Average Days",
    min_value=5,
    max_value=200,
    value=20
)

refresh_seconds = st.sidebar.selectbox(
    "Auto Refresh Interval",
    [5, 10, 15, 30, 60],
    index=1
)

analyze_button = st.sidebar.button(
    "Analyze / Refresh Now",
    type="primary"
)

if st.sidebar.button("Logout"):

    st.session_state.logged_in = False
    st.session_state.email = ""
    st.rerun()


# =====================================
# DATA FETCH AND DASHBOARD
# =====================================

def display_dashboard():

    if not symbol:
        st.warning("Please enter a stock symbol.")
        return

    # Historical mode: one year of daily candles
    if mode == "Historical (1 Year)":
        data = get_stock_data(
            symbol,
            interval="1d",
            period="1y"
        )

    # Intraday mode: one-minute candles
    else:
        data = get_stock_data(
            symbol,
            interval="1m",
            period="1d"
        )

    if data is None or data.empty:
        st.error(
            "Stock data could not be loaded. Check the symbol, "
            "internet connection, and data provider availability."
        )
        return

    required_columns = {
        "date", "open", "high", "low", "close", "volume"
    }

    if not required_columns.issubset(data.columns):
        st.error(
            "Data is missing required columns: date, open, high, "
            "low, close, volume."
        )
        return

    data = data.copy()

    data["date"] = pd.to_datetime(data["date"])
    data.sort_values("date", inplace=True)
    data.reset_index(drop=True, inplace=True)

    # Moving average
    data = calculate_moving_average(
        data,
        int(ma_days)
    )

    # Existing analysis functions
    result = analyze_stock(data)

    latest = data.iloc[-1]
    current_price = float(latest["close"])

    # Reset comparison when symbol changes
    if st.session_state.last_symbol != symbol:
        st.session_state.last_symbol = symbol
        st.session_state.previous_prices.pop(symbol, None)

    previous_price = st.session_state.previous_prices.get(symbol)

    if previous_price is None:
        price_change = None
        direction = "First fetch"
    else:
        price_change = current_price - previous_price

        if price_change > 0:
            direction = "UP ↑"
        elif price_change < 0:
            direction = "DOWN ↓"
        else:
            direction = "UNCHANGED"

    # Save price for the next refresh
    st.session_state.previous_prices[symbol] = current_price

    # =================================
    # STATUS
    # =================================

    st.success(f"{symbol} data loaded successfully.")

    st.caption(
        f"Mode: {mode} | Latest available candle: "
        f"{latest['date']}"
    )

    if mode == "Live / Intraday":
        st.info(
            f"Auto-refresh is enabled every {refresh_seconds} seconds. "
            "The provider may delay prices; refresh does not guarantee "
            "a new market tick."
        )

    # =================================
    # LIVE PRICE AND HIGH-LOW
    # =================================

    st.subheader("Live Price Detection")

    col1, col2, col3, col4 = st.columns(4)

    delta_text = (
        f"{price_change:+.2f}"
        if price_change is not None
        else None
    )

    col1.metric(
        "Latest Available Price",
        f"{current_price:.2f}",
        delta=delta_text
    )

    col2.metric(
        "Latest Candle High",
        f"{float(latest['high']):.2f}"
    )

    col3.metric(
        "Latest Candle Low",
        f"{float(latest['low']):.2f}"
    )

    col4.metric(
        "Latest Candle Volume",
        f"{int(latest['volume']):,}"
    )

    st.write(f"**Price Movement:** {direction}")

    if price_change is not None:
        if current_price != 0:
            pct_change = (
                price_change / previous_price * 100
                if previous_price else 0
            )
        else:
            pct_change = 0

        st.caption(
            f"Change since previous fetch: {price_change:+.2f} "
            f"({pct_change:+.2f}%)"
        )

    # =================================
    # MARKET SUMMARY
    # =================================

    st.subheader("Market Summary")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Current Price",
        f"{result['current']:.2f}"
    )

    col2.metric(
        "Highest Price",
        f"{result['highest']:.2f}"
    )

    col3.metric(
        "Lowest Price",
        f"{result['lowest']:.2f}"
    )

    col4.metric(
        "1 Year Return",
        f"{result['return']:.2f}%"
    )

    # =================================
    # PRICE AND MOVING AVERAGE
    # =================================

    st.subheader("Price and Moving Average")

    chart_data = data.set_index("date")

    st.line_chart(
        chart_data[
            ["close", f"MA{int(ma_days)}"]
        ]
    )

    # =================================
    # CANDLESTICK
    # =================================

    st.subheader("Candlestick Chart")

    candle_fig = candlestick_chart(
        data,
        symbol
    )

    st.pyplot(candle_fig)
    import matplotlib.pyplot as plt
    plt.close(candle_fig)

    # =================================
    # VOLUME
    # =================================

    st.subheader("Trading Volume")

    volume_fig = volume_chart(data)

    st.pyplot(volume_fig)
    plt.close(volume_fig)

    # =================================
    # DETAILED ANALYSIS
    # =================================

    st.subheader("Detailed Analysis")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Average Price",
        f"{result['average']:.2f}"
    )

    col2.metric(
        "Price Range",
        f"{result['range']:.2f}"
    )

    col3.metric(
        "Volatility",
        f"{result['volatility']:.2f}%"
    )

    # =================================
    # HISTORICAL DATA
    # =================================

    st.subheader("Stock Data")

    st.dataframe(
        data,
        use_container_width=True
    )

    # =================================
    # DOWNLOAD CSV
    # =================================

    csv = data.to_csv(index=False)

    st.download_button(
        label="Download CSV",
        data=csv,
        file_name=f"{symbol}_stock_data.csv",
        mime="text/csv"
    )


# =====================================
# AUTO REFRESH
# =====================================

if mode == "Live / Intraday":

    @st.fragment(run_every=f"{refresh_seconds}s")
    def live_dashboard():
        display_dashboard()

    live_dashboard()

else:
    # Historical mode refreshes when the user clicks the button
    if analyze_button:
        with st.spinner("Loading historical stock data..."):
            display_dashboard()
    else:
        st.info(
            "Choose a stock symbol and click "
            "'Analyze / Refresh Now' to load historical data."
        )
