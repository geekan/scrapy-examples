

class ExRule:
    allowed_rule_regex = ''
    # list_css_rules
    paras = {}

    def __init__(self, allowed_rule_regex, **kwargs):
        self.allowed_rule_regex = allowed_rule_regex
        self.paras = kwargs


class BasicConfig:
    name=''
    allowed_domains=[]
    # allowed_url_regex=[]
    start_urls=[]
    ex_rules = []


