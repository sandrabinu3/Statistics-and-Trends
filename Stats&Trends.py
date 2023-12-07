
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


plt.figure(0)
x=ele_cons['Country Name']

y1 = ele_cons['2006']
y2 = ele_cons['2008']
y3 = ele_cons['2010']
y4 = ele_cons['2012']
y5 = ele_cons['2014']
bar_width=0.1
r1=range(len(x))
r2 = [x + bar_width for x in r1]
r3 = [x + bar_width for x in r2]
r4 = [x + bar_width for x in r3]
r5=[x+bar_width for x in r4]
plt.bar(r1, y1, color='b', width=bar_width)
plt.bar(r2, y2, color='r', width=bar_width)
plt.bar(r3, y3, color='g', width=bar_width)
plt.bar(r4, y4, color='y', width=bar_width)   
plt.bar(r5, y5, width=bar_width)
plt.xticks([r + bar_width for r in range(len(x))], x)
plt.legend(['2006', '2008', '2010', '2012','2014'])
plt.title('Electric power consumption')
plt.show()



lst=[]
for i in pro_list:
    a=i[i['Country Name']=='Russian Federation']['2014'].unique()[0]
    lst.append(a)
src_list=['Oil','Nuclear','Natural Gas','Hydroelectric','Other Renewable','Coal']
plt.figure(2)
plt.pie(lst,labels=src_list,autopct='%1.1f%%', startangle=90,explode=(0.1,0,0,0,0.08,0))
plt.title('Electricity production from different sources in Russian Federation')
plt.show()