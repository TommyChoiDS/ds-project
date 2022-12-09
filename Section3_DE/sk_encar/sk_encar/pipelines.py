# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import json
import psycopg2
import sqlite3



class SkEncarPipeline:

    def __init__(self):
        # self.conn = sqlite3.connect('C:/database.db', isolation_level=None)
        # self.c = self.conn.cursor()


        with open('./config.json') as f:
            self.config = json.load(f)

        self.host = self.config['host']
        self.user = self.config['user']
        self.database = self.config['database']
        self.password = self.config['password']

        self.connection = psycopg2.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )

        self.cur = self.connection.cursor()

    def open_spider(self, spider):
        # self.c.execute(
        #     "CREATE TABLE IF NOT EXISTS NEWS_DATA(id INTEGER PRIMARY KEY AUTOINCREMENT, headline text, contents text, parent_link text, article_link text, crawled_time text)")

        self.cur.execute("DROP TABLE IF EXISTS car;")

        self.cur.execute("""
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


    def process_item(self, item, spider):
        # print(item.get('Model'))
        
        self.cur.execute("""INSERT INTO car (Manufacturer, Model, Km, Fuel, Loc, Price, Old_year, Old_month) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s);""", (item.get('Manufacturer'), item.get('Model'),item.get('Km'), item.get('Fuel'), item.get('Loc'), item.get('Price'), item.get('Old_year'), item.get('Old_month')))
        
        return item
        
        
    def close_spider(self, spider):
        self.connection.commit()
        self.connection.close()

        spider.logger.info('TestSpider Pipeline Closed.')
