
from BasicSpiderConfig import ExRule

class Config:

    list_css_rules = { 
        '.cell.item': {
            'title': '.item_title a::text',
            'node': '.node::text',
            'author': '.node+ strong a::text',
            'reply_count': '.count_livid::text'
        }   
    }

    ex_rule = ExRule('http://www.v2ex.com/$', list_css_rules=list_css_rules)

    name='v2ex'
    allowed_domains=['www.v2ex.com']
    start_urls=['http://www.v2ex.com/']
    ex_rules = [ex_rule]

