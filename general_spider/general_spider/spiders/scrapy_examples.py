
from BasicSpiderConfig import ExRule

class Config:

    list_css_rules = { 
        '.js-navigation-item': {
            'content': '.content a::text',
            'message': '.message a::text',
            'age': '.age *::text',
        }   
    }

    ex_rule = ExRule('https://github.com/geekan/scrapy-examples$', list_css_rules=list_css_rules)

    name='scrapy_examples'
    allowed_domains=['github.com']
    start_urls=['https://github.com/geekan/scrapy-examples']
    ex_rules = [ex_rule]

