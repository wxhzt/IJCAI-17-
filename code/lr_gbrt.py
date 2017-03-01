#coding:utf-8
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from sklearn import linear_model
from sklearn.ensemble import GradientBoostingRegressor

from load_data import *
from evaluate import *


upay_daily = pd.read_csv('../dataset/user_pay_count_8_9_10.csv')
preddate = [x.strftime('%Y-%m-%d') for x in pd.date_range('2016-11-01','2016-11-14')]


#特征1
feature1 = pd.DataFrame(np.zeros((2000,len(upay_daily.columns)+14)),index=upay_daily.index,columns=list(upay_daily.columns)+preddate)  
feature1['shop_id'] = upay_daily['shop_id']
for i in range(1,len(feature1.columns)):
    feature1[feature1.columns[i]]= i

#特征2
dateparse = lambda dates: pd.datetime.strptime(dates, '%Y%m%d')
holiday = pd.read_csv('../week/holiday.csv',parse_dates=[0],date_parser=dateparse)
selholiday = holiday[holiday['date']>=datetime(2016,7,31)]
selholiday.index = selholiday.date

feature2 = pd.DataFrame(np.zeros((2000,len(upay_daily.columns)+14)),index=upay_daily.index,columns=list(upay_daily.columns)+preddate)  
feature2['shop_id'] = upay_daily['shop_id']
for i in range(1,len(feature2.columns)):
    feature2[feature2.columns[i]]= list((selholiday.loc[feature2.columns[i]]))[1]


#特征3
feature3 = pd.read_csv('../dataset/isfine.csv')
feature3 = feature3[feature3.columns[:-16]]


#组合特征
features = [feature1,feature2,feature3]
X = []
Y = []
for i in range(2000):
    #for every user
    Y.append([x for x in upay_daily[upay_daily.columns[1:]].iloc[i]])
    dicta = {}
    for k in range(len(features)):
        dicta[k] = features[k][features[k].columns[1:]].iloc[i]
    df = pd.DataFrame(dicta)
    df = df.dropna()

    X.append(np.array(df))

#LR or GBRT 
results = []
for i in range(len(Y)):
    shop_id = i
    #print 'shop '+str(i)
    ytrain = Y[shop_id][40:]
    xtrain = X[shop_id][40:-14]
    xtest = X[shop_id][-14:]
    
    #reg = linear_model.Ridge (alpha = .5)    
    #reg = GradientBoostingRegressor(n_estimators=200, learning_rate=0.05,max_depth=2, random_state=0, loss='ls')
    reg.fit(xtrain, ytrain)
    result = reg.predict(xtest)
    
    #rule1
    mean = upay_daily[upay_daily.columns[1:]].iloc[shop_id][-21:].mean()
    if (np.min(result)<0) :  #如果预测值为负,则为最近21天的平均值
        result = [mean for i in result]

    results.append(result)

#写结果
df = pd.DataFrame(results)
df.index = upay_daily['shop_id']
for col in df.columns:
    df[col] = df[col].apply(int)
df.to_csv('result.csv',header = False)
