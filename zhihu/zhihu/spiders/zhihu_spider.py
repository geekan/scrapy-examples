#coding: utf-8

import re
import json
from urlparse import urlparse


from scrapy.selector import Selector
try:
    from scrapy.spider import Spider
except:
    from scrapy.spider import BaseSpider as Spider
from scrapy.utils.response import get_base_url
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor as sle


from zhihu.items import *
from misc.log import *

'''
1. 默认取sel.css()[0]，如否则需要'__unique':false
2. 默认字典均为css解析，如否则需要'__use':'dump'表明是用于dump数据
'''

class ZhihuSpider(CrawlSpider):
    name = "zhihu"
    allowed_domains = ["zhihu.com"]
    start_urls = [
        "http://www.zhihu.com/",
        "http://www.zhihu.com/people/jia-yang-qing-74",
    ]
    rules = [
        Rule(sle(allow=("/people/[^/]+/followees$")), callback='parse_followees'),
        Rule(sle(allow=("/people/[^/]+/followers$", )), callback='parse_followers'),
        Rule(sle(allow=("/people/[^/]+$", )), callback='parse_people_with_rules', follow=True),
    ]

    # need dfs/bfs
    all_css_rules = {
        '.zm-profile-header': {
            '.zm-profile-header-main': {
                '__use':'dump',
                'name':'.title-section .name::text',
                'sign':'.title-section .bio::text',
                'location':'.location.item::text',
                'business':'.business.item::text',
                'employment':'.employment.item::text',
                'position':'.position.item::text',
                'education':'.education.item::text',
                'education_extra':'.education-extra.item::text',
            }, '.zm-profile-header-operation': {
                '__use':'dump',
                'agree':'.zm-profile-header-user-agree strong::text',
                'thanks':'.zm-profile-header-user-thanks strong::text',
            }, '.profile-navbar': {
                '__use':'dump',
                'asks':'a[href*=asks] .num::text',
                'answers':'a[href*=answers] .num::text',
                'posts':'a[href*=posts] .num::text',
                'collections':'a[href*=collections] .num::text',
                'logs':'a[href*=logs] .num::text',
            },
        }, '.zm-profile-side-following': {
            '__use':'dump',
            'followees':'a.item[href*=followees] strong::text',
            'followers':'a.item[href*=followers] strong::text',
        }
    }

    def traversal(self, sel, rules, item):
        # print 'traversal:', sel, rules.keys()
        if '__use' in rules:
            for nk, nv in rules.items():
                if nk == '__use':
                    continue
                if nk not in item:
                    item[nk] = []
                if sel.css(nv):
                    item[nk] += [i.extract() for i in sel.css(nv)]
                else:
                    item[nk] = []
        else:
            for nk, nv in rules.items():
                for i in sel.css(nk):
                    self.traversal(i, nv, item)

    def dfs(self, sel, rules, item_class):
        if sel is None:
            return []
        item = item_class()
        self.traversal(sel, rules, item)
        return item

    def parse_with_rules(self, response, rules, item_class):
        return self.dfs(Selector(response), rules, item_class)

    def parse_people_with_rules(self, response):
        item = self.parse_with_rules(response, self.all_css_rules, ZhihuPeopleItem)
        item['id'] = urlparse(response.url).path.split('/')[-1]
        info('Parsed '+response.url) # +' to '+str(item))
        return item

    def parse_followers(self, response):
        return self.parse_people_with_rules(response)

    def parse_followees(self, response):
        return self.parse_people_with_rules(response)
