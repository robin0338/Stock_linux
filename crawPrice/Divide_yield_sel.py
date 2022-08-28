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

stock_num = "*"

"""

"""
all_stock = ()
dbname_2 = db_path + 'BWIBBU_2.db'
db2 = sqlite3.connect(dbname_2)
all_stock = pd.read_sql(con=db2, sql="SELECT name FROM sqlite_master WHERE type='table'").values

#all_data = pd.DataFrame()
#all_data = all_data.append(pd.read_sql(con=db2, sql='SELECT * FROM ' + '"' + '2451' + '"'))
#print(all_data['殖利率'].mean().round(decimals=2))
#print(all_data['殖利率'].std().round(decimals=2))

for stock_num in all_stock:
    all_data = pd.DataFrame()
    all_data = all_data.append(pd.read_sql(con=db2, sql='SELECT * FROM ' + '"' + str(stock_num)[1:-1].replace('\'','') + '"'))
    #print('{stock} 平均殖利率為 {test}'.format( stock=str(stock_num)[1:-1].replace('\'','') , test=all_data['殖利率'].mean().round(decimals=2)))
    if all_data['殖利率'].mean().round(decimals=2) > 6 and all_data['殖利率'].std().round(decimals=2) < 2:
        print('{stock} 平均殖利率為 {test}'.format( stock=str(stock_num)[1:-1].replace('\'','') , test=all_data['殖利率'].mean().round(decimals=2)))
