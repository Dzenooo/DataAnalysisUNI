import numpy as np
import seaborn as sns
import pandas as pd

tips = sns.load_dataset("tips")
tips.head()

#print(tips.groupby("day")[['total_bill', 'tip']].agg(['sum', 'mean']))

print(tips.groupby('day')['total_bill'].sum().idxmax())

print(pd.pivot_table(tips, index='day', columns='time', values='tip', aggfunc='mean'))