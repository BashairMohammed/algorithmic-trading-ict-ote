import pandas as pd
import plotly.graph_objects as go
import yfinance as yf

# 1. سحب بيانات حية وحقيقية من ياهو فاينانشال للذهب
ticker = "GC=F"
df = yf.download(ticker, period="60d", interval="1d")

df.columns = [col if isinstance(col, tuple) else col for col in df.columns]

# 2. رصد أعلى قمة وأقل قاع تلقائياً
highest_high = float(df["High"].max())
lowest_low = float(df["Low"].min())
price_range = highest_high - lowest_low

# 3. حساب مستويات الـ ICT Fibonacci
fib_levels = {
    "1.0 (Highest High)": highest_high,
    "0.79 (OTE End)": lowest_low + (price_range * 0.79),
    "0.705 (Sweet Spot)": lowest_low + (price_range * 0.705),
    "0.62 (OTE Start)": lowest_low + (price_range * 0.62),
    "0.50 (Equilibrium)": lowest_low + (price_range * 0.50),
    "0.0 (Lowest Low)": lowest_low,
}

# 4. رسم شارت الشموع اليابانية التفاعلي
fig = go.Figure(
    data=[
        go.Candlestick(
            x=df.index,
            open=df["Open"],
            high=df["High"],
            low=df["Low"],
            close=df["Close"],
            name="Gold Price",
        )
    ]
)

# 5. إسقاط خطوط المستويات على الرسم البياني
colors = ["#ff4d4d", "#ffa500", "#ffd700", "#ffa500", "#1e90ff", "#2ed573"]
for (level_name, price), color in zip(fib_levels.items(), colors):
    fig.add_hline(
        y=price,
        line_dash="dash" if "OTE" in level_name or "Sweet" in level_name else "solid",
        line_color=color,
        annotation_text=f"{level_name}: ${price:,.2f}",
        annotation_position="top right",
    )

fig.update_layout(
    title="Automated Real-Time ICT Fibonacci Retracement (Gold)",
    template="plotly_dark",
    xaxis_rangeslider_visible=False
)
fig.show()
