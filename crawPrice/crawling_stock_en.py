import datetime
import os
import time
import random
import requests
from io import StringIO
import pandas as pd
import numpy as np
import pickle
import configparser
import csv
import sys

"""
Modify Record:
20210522:
    *修改固定的時間參數，改為重外面傳入。
    *增加main function.

"""



"""
Configuration from config.ini
"""
config_file = "./config.ini"
cfp = configparser.ConfigParser()
cfp.read(config_file)

stock_df = cfp['path']['stock_df_en']

#date_st = "2021-05-01"
#date_en = "2021-05-15"


#Function
def crawl_price(date):
    #For Debug
    print('https://www.twse.com.tw/en/exchangeReport/MI_INDEX?response=csv&date=' + date.split(' ')[0].replace('-','') + '&type=ALLBUT0999')

    r = requests.post('https://www.twse.com.tw/en/exchangeReport/MI_INDEX?response=csv&date=' + date.split(' ')[0].replace('-','') + '&type=ALLBUT0999')

    df = pd.read_csv(StringIO("\n".join([i.translate({ord(c): None for c in ' '}) 
                                         for i in r.text.split('\n') 
                                         if len(i.split('",')) == 16 and i[0] != '='])), header=0)
    #save stock data to folder
    df.to_csv(stock_df+date.split(' ')[0].replace('-','')+'.csv',index=None,encoding="utf_8_sig")
    #df.to_pickle(stock_df+date.split(' ')[0].replace('-','')+'.pkl')

def dateRange(start, end, step=1, format="%Y-%m-%d"):
    strptime, strftime = datetime.datetime.strptime, datetime.datetime.strftime
    #print((strptime(end, format) - strptime(start, format)))
    days = (strptime(end, format) - strptime(start, format)).days
    return [strftime(strptime(start, format) + datetime.timedelta(i), format) for i in range(0, days, step)]


#Main function
def main(date_start,date_end):
    date_df = {}
    date_df = dateRange(date_start, date_end)
    fo = open(stock_df+"holiday.txt","a")

    # 使用 crawPrice 爬資料
    for date in date_df:
        date_df_ft = datetime.datetime.strptime(date, "%Y-%m-%d")
        print('parsing', date)
        print('Today is ' + str(datetime.date.isoweekday(date_df_ft)))

        try:
            if os.path.isfile(stock_df+date.split(' ')[0].replace('-','')+'.csv'):
                print(stock_df+date.split(' ')[0].replace('-','') + '.csv' + ' already exist!! \n')
            else:
                #print(stock_df+date.split(' ')[0].replace('-','')+'.csv' + 'already exist!!')
                if((datetime.date.isoweekday(date_df_ft) != 6) & (datetime.date.isoweekday(date_df_ft) != 7)):                  
                    crawl_price(date)
                    print('success! \n')
                    time.sleep(int(random.uniform(3, 5.5)))
                else:
                    print("run else exception")
                    fo.write(date + "\n") 
                    time.sleep(int(random.uniform(3, 5.5)))                   
        except:
            print('fail! check the date is holiday \n')        
            fo.write(date + "  The day is not saturday or sunday" +"\n")    
            time.sleep(int(random.uniform(3, 5.5)))
        #else:
        #    print("run else exception")
        #    fo.write(date + "\n")
        #    time.sleep(0.5)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(len(sys.argv))
        print("Please enter date!!")
    else:    
        main(sys.argv[1],sys.argv[2])



