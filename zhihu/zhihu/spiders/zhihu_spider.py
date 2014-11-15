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
XXX：理论上，可以把所有的css rules都用dict表示（有深度）：

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

1. 默认取sel.css()[0]，如否则需要'__unique':false
2. 默认字典均为css解析，如否则需要'__use':'dump'表明是用于dump数据

'''

class ZhihuCrawlerContext(object):

    def __init__(self, sel=None, css_rules=None):
        self.sel = sel
        self.css_rules = css_rules


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

    def bfs(self, root, func=None):
        cur = [root]
        vals = []
        while cur:
            next = []
            vals.append([x.val for x in cur])
            for i in cur:
                if i.left: next.append(i.left)
                if i.right: next.append(i.right)
            cur = next
        return vals


    def traversal(self, sel, rules, item):
        # print 'traversal:', sel, rules.keys()
        if '__use' in rules:
            for nk, nv in rules.items():
                if nk == '__use':
                    continue
                if sel.css(nv):
                    item[nk] = sel.css(nv)[0].extract()
                else:
                    item[nk] = []
        else:
            for nk, nv in rules.items():
                self.traversal(sel.css(nk)[0], nv, item)

    def dfs(self, sel, rules):
        if sel is None:
            return []
        item = ZhihuPeopleItem()
        self.traversal(sel, rules, item)
        return item

    def parse_with_rules(self, response, rules):
        return self.dfs(Selector(response), rules)

    def parse_people_with_rules(self, response):
        item = self.parse_with_rules(response, self.all_css_rules)
        item['id'] = urlparse(response.url).path.split('/')[-1]
        info('Parsed '+response.url) # +' to '+str(item))
        return item

    def parse_followers(self, response):
        return parse_people(response)

    def parse_followees(self, response):
        return parse_people(response)

    def parse_people(self, response):
        print 'parsed ' + str(response)
        items = []
        sel = Selector(response)

        profile_header = sel.css('.zm-profile-header')[0]

        profile_header_main = profile_header.css('.zm-profile-header-main')[0]
        profile_header_operation = profile_header.css('.zm-profile-header-operation')[0]
        profile_header_navbar = profile_header.css('.profile-navbar')[0]

        profile_side_following = sel.css('.zm-profile-side-following')[0]

        item = ZhihuPeopleItem()
        item['id'] = urlparse(response.url).path.split('/')[-1]

        zhihu_profile_header_main_dict = {
            'name':'.title-section .name::text',
            'sign':'.title-section .bio::text',
            'location':'.location.item::text',
            'business':'.business.item::text',
            'employment':'.employment.item::text',
            'position':'.position.item::text',
            'education':'.education.item::text',
            'education_extra':'.education-extra.item::text',
        }
        zhihu_profile_header_operation_dict = {
            'agree':'.zm-profile-header-user-agree strong::text',
            'thanks':'.zm-profile-header-user-thanks strong::text',
        }
        zhihu_profile_header_navbar = {
            'asks':'a[href*=asks] .num::text',
            'answers':'a[href*=answers] .num::text',
            'posts':'a[href*=posts] .num::text',
            'collections':'a[href*=collections] .num::text',
            'logs':'a[href*=logs] .num::text',
        }
        zhihu_profile_side_following = {
            'followees':'a.item[href*=followees] strong::text',
            'followers':'a.item[href*=followers] strong::text',
        }


        for key, value in zhihu_profile_header_main_dict.items():
            item[key] = [i.extract() for i in profile_header_main.css(value)]

        for key, value in zhihu_profile_header_operation_dict.items():
            item[key] = [i.extract() for i in profile_header_operation.css(value)]

        for key, value in zhihu_profile_header_navbar.items():
            item[key] = [i.extract() for i in profile_header_navbar.css(value)]

        for key, value in zhihu_profile_side_following.items():
            item[key] = [i.extract() for i in profile_side_following.css(value)]

        items.append(item)
        # import pdb; pdb.set_trace()

        return items

    def _process_request(self, request):
        info('process ' + str(request))
        return request
