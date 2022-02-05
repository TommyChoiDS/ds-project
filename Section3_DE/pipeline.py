import re
import requests
from bs4 import BeautifulSoup
import numpy as np
import time
from selenium import webdriver
import pandas as pd
import psycopg2

total_start = time.time()
# --------Extract--------
options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('window-size=1920x1080')
options.add_argument("disable-gpu")

driver = webdriver.Chrome(executable_path = '/usr/local/bin/chromedriver', chrome_options=options)

BASE_URL = 'http://www.encar.com/dc/dc_carsearchlist.do?carType=kor&searchType=model&TG.R=A#!{"action":"(And.Hidden.N._.CarType.Y._.Category.경차.)","toggle":{},"layer":"","sort":"ModifiedDate",'


df = pd.DataFrame(columns = ['Manufacturer' , 'Model', 'Old', 'Km', 'Fuel', 'Loc', 'Price'])

for i in range(1,101): # 100페이지 반복
    start = time.time()
    url = BASE_URL + '"page":%i,"limit":50}' % i 
    page = driver.get(url)
    req = driver.page_source
    time.sleep(3)

    soup = BeautifulSoup(req, 'html.parser')
    print(f'page{i}')
    

    for num in range(1,51):
        tmp_list = []
        tmp_list.append(soup.select(f'#sr_normal > tr:nth-child({num}) > td.inf > a > span.cls > strong')[0].get_text())
        tmp_list.append(soup.select(f'#sr_normal > tr:nth-child({num}) > td.inf > a > span.cls > em')[0].get_text())
        tmp_list.append(soup.select(f'#sr_normal > tr:nth-child({num}) > td.inf > span.detail > span.yer')[0].get_text())
        tmp_list.append(soup.select(f'#sr_normal > tr:nth-child({num}) > td.inf > span.detail > span.km')[0].get_text())
        tmp_list.append(soup.select(f'#sr_normal > tr:nth-child({num}) > td.inf > span.detail > span.fue')[0].get_text())
        tmp_list.append(soup.select(f'#sr_normal > tr:nth-child({num}) > td.inf > span.detail > span.loc')[0].get_text())
        tmp_list.append(soup.select(f'#sr_normal > tr:nth-child({num}) > td.prc_hs > strong')[0].get_text())
                

        df = df.append(pd.Series(tmp_list, index = df.columns), ignore_index = True)
        print(i,"iteration,",num, "data crawling..")
    
    print(i,"page elapsed time:",time.time() - start)

driver.close()


# --------Transformation--------

def toInt(string):
    return int(string.replace(',',''))


def Transformation(df):
    df['Old'] = df['Old'].apply(lambda x : x.split('식')[0])
    df['Old_year'] = pd.to_numeric(df['Old'].apply(lambda x : x.split('/')[0]))
    df['Old_month'] = pd.to_numeric(df['Old'].apply(lambda x : x.split('/')[1]))
    df = df.drop('Old', axis = 1)

    df = df.loc[df['Price'] != '홈서비스 계약중']
    df['Price'] = df['Price'].apply(lambda x : toInt(x))

    df['Km'] = df['Km'].apply(lambda x : x.replace('km','')).apply(lambda x : toInt(x))

    return df

df = Transformation(df)

# --------Load--------


host = 'arjuna.db.elephantsql.com'
user = 'qrnyldng'
password = 'TmCangCbHK1oWFRacELzYlFIDB3pWBYe'
database = 'qrnyldng'

connection = psycopg2.connect(
    host=host,
    user=user,
    password=password,
    database=database
)


cur = connection.cursor()
cur.execute("DROP TABLE IF EXISTS car;")

cur.execute("""
            CREATE TABLE car(
            Manufacturer VARCHAR(20),
            Model VARCHAR(20),
            Km INTEGER,
            Fuel VARCHAR(20),
            Loc VARCHAR(20),
            Price INTEGER,
            Old_year INTEGER,
            Old_month FLOAT
            );
            """)


df = np.array(df)

for i in range(len(df)):
    input = df[i]
    cur.execute("""INSERT INTO car (Manufacturer, Model, Km, Fuel, Loc, Price, Old_year, Old_month) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s);""", input)
    
connection.commit()
print("total elapsed time:", time.time() - total_start)