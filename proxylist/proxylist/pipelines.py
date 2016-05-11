# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import redis


from scrapy import signals


import json
import codecs
from collections import OrderedDict


import sys
import MySQLdb
import hashlib
from scrapy.exceptions import DropItem
from scrapy.http import Request


class JsonWithEncodingPipeline(object):

    def __init__(self):
        self.file = codecs.open('data_utf8.json', 'w', encoding='utf-8')

    def process_item(self, item, spider):
        line = json.dumps(OrderedDict(item), ensure_ascii=False, sort_keys=False) + "\n"
        self.file.write(line)
        return item

    def close_spider(self, spider):
        self.file.close()



class MySQLStorePipeline(object):
    def __init__(self):
        # user, passwd, db
        self.conn = MySQLdb.connect(user='proxylist', passwd='proxylist', db='proxylist', host='localhost', charset="utf8", use_unicode=True)
        self.cursor = self.conn.cursor()
        # self.cursor.execute('create table free_proxy_list (ip varchar(32), port int, code varchar(16), country varchar(64), anoymity varchar(32), google varchar(4), https varchar(4), last_checked varchar(32));''')

    def process_item(self, item, spider):
        try:
            l = ['ip', 'port', 'code', 'country', 'anonymity', 'google', 'https', 'last_checked']
            self.cursor.execute("""
                INSERT INTO free_proxy_list
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
               [item[i].encode('utf-8') for i in l]
            )
            self.conn.commit()
        except MySQLdb.Error, e:
            print "Error %d: %s" % (e.args[0], e.args[1])

        return item


class RedisPipeline(object):

    def __init__(self):
        self.r = redis.StrictRedis(host='localhost', port=6379)

    def process_item(self, item, spider):
        if not item['id']:
            print 'no id item!!'

        str_recorded_item = self.r.get(item['id'])
        final_item = None
        if str_recorded_item is None:
            final_item = item
        else:
            ritem = eval(self.r.get(item['id']))
            final_item = dict(item.items() + ritem.items())
        self.r.set(item['id'], final_item)

    def close_spider(self, spider):
        return
