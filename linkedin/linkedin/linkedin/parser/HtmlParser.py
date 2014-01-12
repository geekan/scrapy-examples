from linkedin.items import PersonProfileItem
from bs4 import UnicodeDammit
from w3lib.url import url_query_cleaner
import random
import LinkedinParser


class HtmlParser:    
    @staticmethod
    def extract_person_profile(hxs):
        personProfile = PersonProfileItem()
        ## Person name
        nameField = {}
        nameSpan = hxs.select("//span[@id='name']/span")
        if nameSpan and len(nameSpan) == 1:
            nameSpan = nameSpan[0]
            givenNameSpan = nameSpan.select("span[@class='given-name']")
            if givenNameSpan and len(givenNameSpan) == 1:
                givenNameSpan = givenNameSpan[0]
                nameField['given_name'] = givenNameSpan.select("text()").extract()[0]
            familyNameSpan = nameSpan.select("span[@class='family-name']")
            if familyNameSpan and len(familyNameSpan) == 1:
                familyNameSpan = familyNameSpan[0]
                nameField['family_name'] = familyNameSpan.select("text()").extract()[0]
            personProfile['name'] = nameField
        else:
            return None
        
        headline = hxs.select("//dl[@id='headline']")
        if headline and len(headline) == 1:
            headline = headline[0]
            ## locality
            locality = headline.select("dd/span[@class='locality']/text()").extract()
            if locality and len(locality) == 1:
                personProfile['locality'] = locality[0].strip()
            ## industry
            industry = headline.select("dd[@class='industry']/text()").extract()
            if industry and len(industry) == 1:
                personProfile['industry'] = industry[0].strip()
        
        ## overview
        overview = hxs.select("//dl[@id='overview']").extract()
        if overview and len(overview) == 1:
            personProfile['overview_html'] = overview[0]
            homepage = LinkedinParser.parse_homepage(overview[0])
            if homepage:
                personProfile['homepage'] = homepage
            
        ## summary
        summary = hxs.select("//div[@id='profile-summary']/div[@class='content']/p[contains(@class,'summary')]/text()").extract()
        if summary and len(summary) > 0:
            personProfile['summary'] = ''.join(x.strip() for x in summary)
        
        ## specilities
        specilities = hxs.select("//div[@id='profile-specialties']/p/text()").extract()
        if specilities and len(specilities) == 1:
            specilities = specilities[0].strip()
            personProfile['specilities'] = specilities
        
        ## skills
        skills = hxs.select("//ol[@id='skills-list']/li/span/a/text()").extract()
        if skills and len(skills) > 0:
            personProfile['skills'] = [x.strip() for x in skills]
            
        additional = hxs.select("//div[@id='profile-additional']")
        if additional and len(additional) == 1:
            additional = additional[0]
            ## interests
            interests = additional.select("div[@class='content']/dl/dd[@class='interests']/p/text()").extract()
            if interests and len(interests) == 1:
                personProfile['interests'] = interests[0].strip()
            ## groups
            g = additional.select("div[@class='content']/dl/dd[@class='pubgroups']")
            if g and len(g) == 1:
                groups = {}
                g = g[0]
                member = g.select("p/text()").extract()
                if member and len(member) > 0:
                    groups['member'] = ''.join(member[0].strip())
                gs = g.select("ul[@class='groups']/li[contains(@class,'affiliation')]/div/a/strong/text()").extract()
                if gs and len(gs) > 0:
                    groups['affilition'] = gs
                personProfile['group'] = groups
            ## honors
            honors = additional.select("div[@class='content']/dl/dd[@class='honors']/p/text()").extract()
            if honors and len(honors) > 0:
                personProfile['honors'] = [x.strip() for x in honors]
        
        ## education
        education = hxs.select("//div[@id='profile-education']")
        schools = []
        if education and len(education) == 1:
            education = education[0]
            school_list = education.select("div[contains(@class,'content')]//div[contains(@class,'education')]")
            if school_list and len(school_list) > 0:
                for school in school_list:
                    s = {}
                    name = school.select("h3[contains(@class,'org')]/text()").extract()
                    if name and len(name) == 1:
                        s['name'] = name[0].strip()
                    degree = school.select("h4[@class='details-education']/span[@class='degree']/text()").extract()
                    if degree and len(degree) == 1:
                        s['degree'] = degree[0].strip()
                    major = school.select("h4[@class='details-education']/span[@class='major']/text()").extract()
                    if major and len(major) == 1:
                        s['major'] = major[0].strip()
                    period = school.select("p[@class='period']")
                    if period and len(period) == 1:
                        period = period[0]
                        start = period.select("abbr[@class='dtstart']/text()").extract()
                        end = period.select("abbr[@class='dtend']/text()").extract()
                        if len(start) == 1:
                            s['start'] = start[0]
                        if len(end) == 1:
                            s['end'] = end[0]
                    desc = school.select("p[contains(@class,'desc')]/text()").extract()
                    if len(desc) == 1:
                        s['desc'] = desc[0].strip()
                    schools.append(s)
                personProfile['education'] = schools 
        
        ## experience
        experience = hxs.select("//div[@id='profile-experience']")
        if experience and len(experience) == 1:
            es = []
            experience = experience[0]
            exps = experience.select("//div[contains(@class,'experience')]")
            if len(exps) > 0:
                for e in exps:
                    je = {}
                    title = e.select("div[@class='postitle']//span[@class='title']/text()").extract()
                    if len(title) > 0:
                        je['title'] = title[0].strip()
                    org = e.select("div[@class='postitle']//span[contains(@class,'org')]/text()").extract() 
                    if len(org) > 0:
                        je['org'] = org[0].strip()
                    start = e.select("p[@class='period']/abbr[@class='dtstart']/text()").extract()
                    if len(start) > 0:
                        je['start'] = start[0].strip()
                    end = e.select("p[@class='period']/abbr[@class='dtstamp']/text()").extract()
                    if len(end) > 0:
                        je['end'] = end[0].strip()
                    location = e.select("p[@class='period']/abbr[@class='location']/text()").extract()
                    if len(location) > 0:
                        je['location'] = location[0]
                    desc = e.select("p[contains(@class,'description')]/text()").extract()
                    if len(desc) > 0:
                        je['desc'] = "".join(x.strip() for x in desc)
                    es.append(je)
            personProfile['experience'] = es
                    
        ## Also view
        alsoViewProfileList = []
        divExtra = hxs.select("//div[@id='extra']")
        if divExtra and len(divExtra) == 1:
            divExtra = divExtra[0]
            divAlsoView = divExtra.select("//div[@class='leo-module mod-util browsemap']")
            if divAlsoView and len(divAlsoView) == 1:
                divAlsoView = divAlsoView[0]
                alsoViewList = divAlsoView.select("div[@class='content']/ul/li/strong/a/@href").extract()
                if alsoViewList:
                    for alsoViewItem in alsoViewList:
                        alsoViewItem = UnicodeDammit(alsoViewItem).markup
                        item = HtmlParser.get_also_view_item(alsoViewItem)
                        alsoViewProfileList.append(item)
                    personProfile['also_view'] = alsoViewProfileList
        return personProfile

    @staticmethod
    def get_also_view_item(dirtyUrl):
        item = {}
        url = HtmlParser.remove_url_parameter(dirtyUrl)
        item['linkedin_id'] = url 
        item['url'] = HtmlParser.get_linkedin_id(url)
        return item
        
        
    @staticmethod
    def remove_url_parameter(url):
        return url_query_cleaner(url)
    
    @staticmethod
    def get_linkedin_id(url):
        find_index = url.find("linkedin.com/")
        if find_index >= 0:
            return url[find_index + 13:].replace('/', '-')
        return None
        
