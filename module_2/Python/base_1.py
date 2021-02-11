# from https://towardsdatascience.com/3-basic-steps-of-stock-market-analysis-in-python-917787012143

## get stock data

pip install yfinance

df = yf.download("TSLA", start="2018-11-01", end="2020-10-18", interval="1d")df.head()

## Calculate trading indicators

### Moving average

pip install TA-Lib

df.loc[:, 'ma20'] = df.Close.rolling(20).mean()
df.loc[:, 'ma200'] = df.Close.rolling(200).mean()

### RSI: Relative strength index

import talibdf.loc[:, "rsi"] = talib.RSI(df.Close, 14)

import matplotlib.pyplot as pltfig, ax = plt.subplots(1, 2, figsize=(21, 7))ax0 = df[["rsi"]].plot(ax=ax[0])
ax0.axhline(30, color="black")
ax0.axhline(70, color="black")df[["Close"]].plot(ax=ax[1])

## Visualization


pip install plotly

import plotly.graph_objects as gofig = go.Figure(
    data=go.Ohlc(
        x=df.index,
        open=df["Open"],
        high=df["High"],
        low=df["Low"],
        close=df["Close"],
    )
)
fig.show()

