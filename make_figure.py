import matplotlib.pyplot as plt
import pandas as pd
import requests
from datetime import datetime
from jupyterthemes import jtplot

jtplot.style(theme="onedork")

url = "https://api.blockchain.info/charts/market-price?timespan=all"
data = requests.get(url).json()
df = pd.DataFrame(data["values"])

url_current_price = "https://data-api.coindesk.com/index/cc/v1/latest/tick?market=ccix&instruments=BTC-USD"
data_cp = requests.get(url_current_price).json()
cp = float(data_cp["Data"]["BTC-USD"]["VALUE"])
ct = datetime.now()

df = pd.concat([df, pd.DataFrame(data=[[ct.timestamp(),cp]], columns=["x", "y"])], ignore_index=True)

df.columns = ["Date", "USD/BTC"]
df["Date"] = pd.to_datetime(df["Date"], unit="s")
df = df.set_index("Date")

df["Max"] = df["USD/BTC"].max()
imax = df["USD/BTC"].idxmax()
df["local_Min"] = df["USD/BTC"][imax:].min()

ax = df["2010-11":].plot(logy=True, drawstyle="steps", figsize=(16, 6))

ax.annotate(df["USD/BTC"][imax], xy=("2012-11", df["USD/BTC"][imax]), color="g")
ax.axvline(imax, color="g")

lmi = df["USD/BTC"][imax:].idxmin()
ax.annotate(df["USD/BTC"][lmi], xy=("2012-11", df["USD/BTC"][lmi]), color="r")
ax.axvline(lmi, color="r")

ax.get_figure().savefig("bitcoin-all.svg", bbox_inches="tight")

ix = df["USD/BTC"][df["USD/BTC"] > df["local_Min"]].index
if len(ix) > 2:
    start = ix[0]
else:
    start = "2017-9"
plt.clf()
df[start:]["USD/BTC"].plot(drawstyle="steps", figsize=(16, 6)).get_figure().savefig(
    "bitcoin-lastlinear.svg", bbox_inches="tight"
)
