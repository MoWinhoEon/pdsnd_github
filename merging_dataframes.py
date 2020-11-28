import time
import pandas as pd
import numpy as np

df1 = pd.read_csv("chicago.csv")
df2 = pd.read_csv("new_york_city.csv")
df3 = pd.read_csv("washington.csv")

# Create a column with the city name
df1['City'] = 'chicago'
df2['City'] = 'new_york_city'
df3['City'] = 'washington'

# changing dtypes of washington to the ones of the others and create missing columns
df3['Trip Duration'] = df3['Trip Duration'].astype(int)
df3['Gender'] = 'Unknown'
df3['Birth Year'] = np.nan

# merge dataframes
frames = [df1, df2, df3]
df = pd.concat(frames, sort = False)

# export as csv
df.to_csv(r'all_cities.csv')
