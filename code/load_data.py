#coding:utf-8
import numpy as np
import pandas as pd
from datetime import datetime
def load_data():
    print 'load user_pay ...'
    dateparse = lambda dates: pd.datetime.strptime(dates, '%Y-%m-%d %H:%M:%S')
    upay = pd.read_csv('../dataset/user_pay_8_9_10.csv',parse_dates=[2],date_parser=dateparse)
    print 'load user_view ...'
    dateparse = lambda dates: pd.datetime.strptime(dates, '%Y-%m-%d %H:%M:%S')
    uview= pd.read_csv('../dataset/user_view_8_9_10.csv',parse_dates=[2],date_parser=dateparse)
    print 'load shop info ...'
    shop = pd.read_csv('../dataset/shop_info.csv',header=-1)
    shop.columns = ['shop_id','city_name','location_id','per_pay','score','comment_cnt','shop_level','cate_1_name','cate_2_name','cate_3_name']
    print 'load every day count ...'
    upay_daily = pd.read_csv('../dataset/user_pay_count_8_9_10.csv')
    
 

    return upay, uview, shop, upay_daily

