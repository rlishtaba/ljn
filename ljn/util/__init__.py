#coding:utf-8

def word_count(data):
    import re
    return len(re.findall(ur"[\w\-,\.'%s]+" % u'\u2019', data))
