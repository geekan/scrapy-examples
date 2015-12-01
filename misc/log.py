
#from scrapy import log
import logging as log

def warn(msg):
    #log.msg(str(msg), level=log.WARNING)
    log.warn(str(msg))


def info(msg):
    #log.msg(str(msg), level=log.INFO)
    log.info(str(msg))


def debug(msg):
    #log.msg(str(msg), level=log.DEBUG)
    log.debug(str(msg))

import pprint
class MyPrettyPrinter(pprint.PrettyPrinter):
    def format(self, object, context, maxlevels, level):
        if isinstance(object, unicode):
            return (object.encode('utf8'), True, False)
        return pprint.PrettyPrinter.format(self, object, context, maxlevels, level)
pu = MyPrettyPrinter()

pp = pprint.PrettyPrinter()
