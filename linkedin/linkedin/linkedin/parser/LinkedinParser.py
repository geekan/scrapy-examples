from bs4 import BeautifulSoup
from urllib2 import urlparse

def parse_homepage(html):
    soup = BeautifulSoup(html)
    websites = soup.find_all('dd', 'websites')
    if websites and len(websites) > 0:
        websites = websites[0]
        sites = websites.find_all('li')
        if sites and len(sites) > 0:
            result = {}
            for site in sites:
                site_name = site.text.strip()
                original = site.a.get('href')
                url_parse = urlparse.urlparse(original).query
                query_parse = urlparse.parse_qs(url_parse)
                if 'url' in query_parse:
                    result[site_name] = query_parse['url']
            return result
    return None

