import os
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
_res = db.search(
    (Language.techno == "amoa")
    | (Language.techno == "python")
    | (Language.techno == "java")
    | (Language.techno == "chef de projet")
    | (Language.techno == "supply chain")
    | (Language.techno == "solidity")
    | (Language.techno == "power bi")
    | (Language.techno == "react")
    | (Language.techno == "vue")
)


df = pd.DataFrame(_res)


def date_to_nb(curr_date):
    return datetime.strptime(curr_date, "%Y/%m/%d-%H:%M:%S").timetuple().tm_yday


def convert_to_nb_week(data):
    return floor(data / 7)


df["date"] = df["date"].apply(date_to_nb)
df["no_week"] = df["date"].apply(convert_to_nb_week)
df = df.pivot("date", "techno", "total")
sns.set()

res = sns.lineplot(data=df, markers=True)
plt.title("Evolution nb techno")
plt.show()
