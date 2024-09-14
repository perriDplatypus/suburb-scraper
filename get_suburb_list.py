""" Fetches suburb list from the sheet csv """

import pandas as pd

sheet = pd.read_csv("./source.csv")
sheet["Suburb"].to_csv("./suburbs.csv", encoding='utf-8', index=False)
