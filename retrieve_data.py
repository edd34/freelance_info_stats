import os
from datetime import datetime
from pprint import pprint
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from tinydb import Query, TinyDB
from dotenv import load_dotenv

load_dotenv()

db = TinyDB("db.json")
Language = Query()
fig = plt.figure()
_res = db.search(
    (Language.techno == "amoa")
    | (Language.techno == "python")
    | (Language.techno == "java")
)


df = pd.DataFrame(_res)
df = df.pivot("date", "techno", "total")

sns.set()

res = sns.lineplot(data=df)
plt.title("Evolution nb techno")
plt.show()
