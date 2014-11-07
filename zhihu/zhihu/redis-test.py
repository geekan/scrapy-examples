
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
        except:
            pass
    return pairs

def main():
    print json.dumps(dump_all(), indent=4)

if __name__ == '__main__':
    main()
