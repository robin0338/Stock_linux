# -*- encoding: utf8-*-
import datetime
import time
import random
import requests
from io import StringIO
import pandas as pd
import numpy as np
import pickle
import configparser
import csv
import os

"""
Configuration from config.ini
"""
config_file = "./config.ini"
cfp = configparser.ConfigParser()
cfp.read(config_file)

BWIBBU = cfp['path']['BWIBBU']

#Function
def crawl_bwibbu(date1,date2):
    #For Debug
    print(r"https://www.twse.com.tw/exchangeReport/TWT49U?response=csv&strDate="+ date1 + "&endDate=" + date2 )

    r = requests.post("https://www.twse.com.tw/exchangeReport/TWT49U?response=csv&strDate="+ date1 + "&endDate=" + date2 )

    df = pd.read_csv(StringIO("\n".join([i.translate({ord(c): None for c in ' '}) for i in r.text.split('\n') if len(i.split(',')) == 16])), header=0)

    df['殖利率'] = df['權值+息值']/df['除權息前收盤價']*100
    df['殖利率'] = df['殖利率'].round(decimals=2)
    if os.path.isfile(BWIBBU+date1[:4]+'.csv'):
        print(BWIBBU+date1[:4]+'.csv' + ' already exist!!')
    else:
        df.to_csv(BWIBBU+date1[:4]+'.csv',encoding="utf_8_sig")
def dateRange(start, end, step=1, format="%Y-%m-%d"):
    strptime, strftime = datetime.datetime.strptime, datetime.datetime.strftime
    print((strptime(end, format) - strptime(start, format)))
    days = (strptime(end, format) - strptime(start, format)).days
    return [strftime(strptime(start, format) + datetime.timedelta(i), format) for i in range(0, days, step)]

crawl_bwibbu("20190101","20191231")
crawl_bwibbu("20180101","20181231")
crawl_bwibbu("20170101","20171231")
crawl_bwibbu("20160101","20161231")
crawl_bwibbu("20150101","20151231")
crawl_bwibbu("20140101","20141231")
crawl_bwibbu("20130101","20131231")
crawl_bwibbu("20120101","20121231")
crawl_bwibbu("20110101","20111231")
crawl_bwibbu("20100101","20101231")


