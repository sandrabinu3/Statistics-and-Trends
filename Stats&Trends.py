
import pandas as pd 
import numpy as np
import matplotlib.pyplot as pyplot
import seaborn as sns

def readFile(filename,cntry_list,indicator):
    df=pd.read_excel(filename,skiprows=2,header=1)
    ref_df=df[(df['Country Name'].isin(cntry_list)) & (df['Indicator Name']==indicator)]
    ref_df=ref_df.drop(df.columns[1:4],axis=1)
    yr=[str(year) for year in range(1960,2011)] + [str(year) for year in range(2021,2023)]
    final_df=ref_df.drop(columns=yr)
    final_df=final_df.reset_index(drop=True)
    trans_df=final_df.transpose()
    trans_.columns=trans_df.iloc[0]
    trans_df=trans_df[1:]
    trans_df.index.names=['Years']
    return final_df,trans_df