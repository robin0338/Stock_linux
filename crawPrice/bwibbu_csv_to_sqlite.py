import sqlite3
import glob
import os
import csv
import configparser
import pandas as pd

"""
Configuration from config.ini
"""
config_file = "./config.ini"
cfp = configparser.ConfigParser()
cfp.read(config_file)

db_path = cfp['path']['database']
BWIBBU = cfp['path']['BWIBBU']

"""
Read csv file from specific folder
"""
all_stock_data = glob.glob(BWIBBU + "/*.csv")


"""
Create sql database
"""
dbname = db_path + 'BWIBBU.db'

dates_list = []
#連接到我們的資料庫，如果沒有的話會重新建一個
db = sqlite3.connect(dbname)
for files in all_stock_data:
    dates_list.append(os.path.basename(files).replace('.csv',''))
    #print(os.path.basename(files).replace('.csv',''))
    pd.read_csv(files).to_sql(os.path.basename(files).replace('.csv',''),db,if_exists='replace')

total_df = pd.DataFrame()
for date in dates_list:
    df = pd.read_sql(con = db, sql = 'SELECT * FROM' + '"' + date + '"')
    df['Date'] = date
    total_df = total_df.append(df)

#print(total_df)

#Create second database for 
dbname_2 = db_path + 'BWIBBU_2.db'
db2 = sqlite3.connect(dbname_2)
total_df['股票代號'] = total_df['股票代號'].str.replace('=','')
total_df['股票代號'] = total_df['股票代號'].str.replace('"','')
total_dict = dict(tuple(total_df.groupby('股票代號')))
#print(total_dict)


for key in total_dict.keys():
    #print(key)
    df = total_dict[key]
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.sort_values(by=['Date'])
    df.to_sql(key,db2,if_exists='replace')



