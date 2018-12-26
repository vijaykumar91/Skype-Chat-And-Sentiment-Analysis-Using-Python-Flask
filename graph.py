import numpy as np
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns
import missingno as msno

#======================================================================================================
# Build DataFrame from scratch


# Load transactions
df = pd.read_excel('file:///C:/Users/abc/Downloads/Google form test data.xlsx')

#null_columns=df.columns[df.isnull().any()]
#df.fillna(1)

#print(df)
dates=df['Date']
for col in dates:
    #print(col)
    #print(pd.to_datetime(col))
    if(isinstance(col, str)):
        newdate=col.split("/")
        day=newdate[0]
        month = newdate[1]
        year1 = newdate[2]
        year=year1[-2:]
        nowNewDate=day+'-'+month+'-20'+year
        #print(nowNewDate)
        df['Date'] = nowNewDate
    else:
       df['Date']= pd.to_datetime(col).date()

        #a_date_object = datetime.strptime(col)
        # a_date_object = pd.to_datetime(col, dayfirst=True, format="%d-%b-%y %H:%M:%S")
        #print(col)

        #df['Date']= pd.to_datetime(col).date()

#print(df['Date'])
#dfST['timestamp'] = pd.to_datetime(dfST['timestamp'])
#pd.to_datetime(df['Date'], coerce=True)
# Take a look at the first few rows

# print(df['Delivery Fare'])
# print(df['Delivery Fare'].isnull())
# cnt=0
# for row in df['Delivery Fare']:
#     try:
#         int(row)
#         df.loc[cnt, 'Delivery Fare']=np.nan
#     except ValueError:
#         pass
#     cnt+=1
#print (df.isnull().values.any())
#print(df.isnull().sum())
#print(df.isnull().sum().sum())
#median = df.head()
#print(median)
# #df['Delivery Fare'].fillna(median, inplace=True)
# df['median_fare']=median
# df.to_csv('out2.csv')


#df=df.shape
# df=df.isnull()
# df=df.isnull().sum()
# df[col].isnull().sum()
# print(df)

# wine.head()
# wine.info()
# fig = plt.figure(figsize = (10,6))
# sns.barplot(x = 'Id', y = 'Drone Type', data = wine)
# #df.sort_values(['id','val']).groupby('id').ffill()

# df = pd.DataFrame({m: ser.interpolate(method=m) for m in methods})
# (sns.heatmap(df.isnull()))
# (msno.matrix(df))
# msno.heatmap(df)