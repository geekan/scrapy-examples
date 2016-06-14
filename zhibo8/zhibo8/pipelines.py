# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import MySQLdb
from utils.mysqldriver import MySQL

class SportPipeline(object):
    _db = None

    def __init__(self):
        dbconfig = {
          'host':'localhost', 
          'port': 3306, 
          'user':'root', 
          'passwd':'111111', 
          'db':'sport', 
          'charset':'utf8'
        }
    
        self._db = MySQL(dbconfig)

    def process_item(self, item, spider):    
        insert_sql = "INSERT INTO sport_schedule(home_team,guest_team,home_logo,guest_logo,match_date,game_type) values \
                      ('%s','%s','%s','%s','%s','%s')" % (item['home_team'], item['guest_team'], item['home_logo'],\
                      item['guest_logo'], item['match_date'], item['game_type'])

        self._db.insert(insert_sql)
        return item
