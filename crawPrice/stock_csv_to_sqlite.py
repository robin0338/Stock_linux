import sqlite3
import glob
import os
import sys
import csv
import configparser
import pandas as pd

"""
20210530:
    * 增加 thousands=r','在讀取csv時。
    
"""


"""
Configuration from config.ini
"""
config_file = "./config.ini"
cfp = configparser.ConfigParser()
cfp.read(config_file)

db_path = cfp['path']['database']
#已修改為英文版
stock_df = cfp['path']['stock_df_en']

"""
Create sql database
"""
def cre_db(sel_year):
    dbname = db_path + sel_year + '.db'
    dates_list = []
    global total_df
    """
    Read csv file from specific folder
    """
    #sel_year = '2016'
    all_stock_data = glob.glob(stock_df + "/" + sel_year + "*.csv")
    #print(all_stock_data)    

    #連接到我們的資料庫，如果沒有的話會重新建一個
    #generate a dataframe name by date(ex:20190102) to db database.
    #Table name by csv file name.
    db = sqlite3.connect(dbname)
    for files in all_stock_data:
        print('This is {csv} files.'.format(csv=files))
        #Get date from file name.
        dates_list.append(os.path.basename(files).replace('.csv',''))
        pd.read_csv(files, thousands=r',').to_sql(os.path.basename(files).replace('.csv',''),db,if_exists='replace')
    #read sql database we just create, then append date table to last dateframe column.
    total_df = pd.DataFrame()
    for date in dates_list:
        df = pd.read_sql(con = db, sql = 'SELECT * FROM' + '"' + date + '"')
        df['Date'] = date
        total_df = total_df.append(df)

    #Create second database for reorder.
    dbname_2 = db_path + sel_year + '_order' + '.db'
    db2 = sqlite3.connect(dbname_2)
    #Regroup stock information by stock number.
    total_dict = dict(tuple(total_df.groupby('SecurityCode')))

    for key in total_dict.keys():
        df = total_dict[key].iloc[:,2:]
        print(pd.to_datetime(df['Date']))
        #轉換為正常的日期格式
        df['Date'] = pd.to_datetime(df['Date'])
        #重新將日期做排序
        df = df.sort_values(by=['Date'])
        print('This is {key}'.format(key=key))
        df.to_sql(key,db2,if_exists='replace')


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(len(sys.argv))
        print("Please enter date!!")
    else:    
        for x in range(int(sys.argv[1]),int(sys.argv[2])+1):
            cre_db(str(x))  
        






