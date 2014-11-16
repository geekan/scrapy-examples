#!/usr/bin/env python

import redis
import json


r = redis.StrictRedis(host='localhost', port=6379)


def dump_all(redis=r):
    keys = redis.keys('*')
    pairs = {}
    for key in keys:
        type = redis.type(key)
        val = redis.get(key)
        try:
            pairs[key] = eval(val)
        except Exception as e:
            print pairs, key, val, e
    return pairs

def del_all(redis=r):
    keys = redis.keys('*')
    for k in keys:
        print 'Deleting:', k, 'result is', redis.delete(k)

def main():
    # del_all()
    # print json.dumps(dump_all(), indent=4)
    keys = r.keys('*')
    print keys
    print len(keys)

if __name__ == '__main__':
    main()
