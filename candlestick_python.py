import os
import plotly.graph_objects as go
from math import floor
from datetime import datetime
from pprint import pprint

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from dotenv import load_dotenv
from tinydb import Query, TinyDB

load_dotenv()

db = TinyDB("db.json")
Language = Query()
fig = plt.figure()
_res = db.search((Language.techno == "python"))


df = pd.DataFrame(_res)


def date_to_nb(curr_date):
    return datetime.strptime(curr_date, "%Y/%m/%d-%H:%M:%S").timetuple().tm_yday


def convert_to_nb_week(data):
    return floor(data / 7)


df["date"] = df["date"].apply(date_to_nb)
df["no_week"] = df["date"].apply(convert_to_nb_week)

tmp = df.groupby(["no_week"])
_high = tmp.apply(lambda x: np.max(x["total"]))
_low = tmp.apply(lambda x: np.min(x["total"]))
_mean = tmp.apply(lambda x: np.round(np.mean(x["total"])))
_median = tmp.apply(lambda x: np.round(np.median(x["total"])))
_first = tmp.first()["total"]
_last = tmp.last()["total"]


res = pd.concat(
    [
        pd.DataFrame(_high),
        pd.DataFrame(_low),
        pd.DataFrame(_first),
        pd.DataFrame(_last),
        pd.DataFrame(_mean),
        pd.DataFrame(_median),
    ],
    axis=1,
)


res.columns = ["high", "low", "open", "close", "mean", "median"]
res = res.iloc[1:]
print(res)

fig = go.Figure(
    data=[
        go.Candlestick(
            x=res.index,
            open=res["open"],
            high=res["high"],
            low=res["low"],
            close=res["close"],
        )
    ]
)

fig.show()
