# encoding:utf8
"""
zhibo8比分
"""
import scrapy
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )

game_type_list = [
        u'CBA', 
        u'NBA', 
        u'法甲', 
        u'英超', 
        u'西甲', 
        u'意甲', 
        u'德甲', 
        u'足总杯', 
        u'国王杯', 
        u'德国杯', 
        u'解放者杯',
        u'意大利杯',
 ] 


class Zhibo8ScheduleSpider(scrapy.Spider):
    name = "zhibo8_schedule"
    allowed_domains = ["zhibo8.cc"]
    start_urls = ["http://zhibo8.cc/"]

    def parse(self, response):
        arr_matches = []
        # refer : http://scrapy-chs.readthedocs.org/zh_CN/0.24/topics/selectors.html#topics-selectors-relative-xpaths
        div_list = response.xpath('//div[@class="schedule_container left"]/div[@class="box"]')
        for div in div_list:
            match_date = div.xpath('div[@class="titlebar"]/h2[1]/@title').extract()[0]
            li_list = div.xpath('div[@class="content"]/ul/li')
            ymd = match_date.replace('-', '')
            for li in li_list:
                match = {}
                match['tags'] = li.xpath('./@label').extract()[0]
                text_content = li.xpath('string(.)').extract()[0]
                text_content = text_content.replace('  ', ' ')
                arr_content = text_content.split(' ')
                #print 0,arr_content[0],1,arr_content[1],2,arr_content[2],3,arr_content[3],4,arr_content[4],\
                #        5,arr_content[5],6,arr_content[6],7,arr_content[7]
                if len(arr_content) < 5 or '-' != arr_content[3]:
                    continue
                match['start_time'] = match_date + ' ' + arr_content[0] + ':00'
                match['home_team']  = arr_content[2]
                match['guest_team'] = arr_content[4]
                match['match_date'] = ymd
                match['game_type']  = self.get_gametype(arr_content[1])
                match['home_logo']  = self.get_home_logo(li)
                match['guest_logo'] = self.get_guest_logo(li)
                #print match['start_time'],match['home_team'],match['guest_team'],match['home_logo'],match['guest_logo']
                arr_matches.append(match)

        return arr_matches


    def get_gametype(self, s):
        for game_type in game_type_list:
            if game_type in s:
                return game_type
        return s


    def get_home_logo(self, li):
        if li.xpath('./img[1]'):
            return li.xpath('./img[1]/@src').extract()[0]
        elif li.xpath('./b/img[1]'):
            return li.xpath('./b/img[1]/@src').extract()[0]
        else:
            return ''

    def get_guest_logo(self, li):
        if li.xpath('./img[2]'):
            return li.xpath('./img[2]/@src').extract()[0]
        elif li.xpath('./b/img[2]'):
            return li.xpath('./b/img[2]/@src').extract()[0]
        else:
            return ''

