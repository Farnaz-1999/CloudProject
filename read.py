import csv
import pandas as pd

pName='Baked'

data= pd.read_csv("./data/planes.csv")

if pName in data['0'].to_list():
    data.loc[data[data['0']==pName].index.values,'1']=int(data.loc[data[data['0']==pName].index.values,'1'].values)-1

data.to_csv('./data/planes.csv', index=False)
