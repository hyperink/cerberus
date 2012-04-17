#!/usr/bin/python
# -*- coding: utf-8 -*-
from contextlib import closing
import xml_utils
import urllib
import urllib2
import requests
from cStringIO import StringIO

DEFAULT_FILE = "examples/copyscape_example.xml"

def test_xml(fn=DEFAULT_FILE):
    with closing(open(fn)) as f:
        return f.read()

def xml_from_url(url):
    """ url -> xml
    """
    return test_xml()

def file_content(content):
    return StringIO(content)

def xml_from_content(content):
    """ content -> xml """
    url = url_content(content)
    data = data_content(content)
    r = requests.post(url, data=data)
    return r.text

def data_content(content, url="http://www.copyscape.com/api", username="hyperink", 
                 key="yy10ol2l6yapyo0w5", method="csearch", encoding="UTF-8", format="xml"):
    data = {
        "u": username,
        "t": content,
        "k": key,
        "o": method,
        "e": encoding,
        "c": 3,
        "f": format
    }
    return data

def url_content(content, url="http://www.copyscape.com/api/"):
    return url

def dict_from_xml(xml):
    """
    xml -> dictionary
    """
    return xml_utils.xmltodict(xml.encode('utf-8'))

def test():
    d = dict_from_xml(xml_from_url(None))
    return d

def content_filename(filename):
    """ filename -> content """
    with closing(open(filename)) as f:
        return f.read()

def test_content(filename="examples/raw.txt"):
    content = content_filename(filename)
    d = dict_from_xml(xml_from_content(content))
    return d

def metric_content(content):
    """
    text -> metric
    """
    return metric_dict(dict_from_xml(xml_from_content(content)))


def metric_filename(filename):
    """
    File on disk -> metric
    """
    return metric_dict(dict_from_xml(xml_from_content(content_filename(filename))))


def metric_dict(dict_results):
    """ 
    results is a dict of the xml
    \Sigma_{i=0}^{n} 1/n^2 * mwf/wc
    """
    wc = wc_results(dict_results)
    mwm = mwm_results(dict_results)
    return sum(((n + 1)**-2 * mwf / wc for n, mwf in enumerate(mwm)))

def unwrap(string_in_list):
    """ [u'26'] -> 26 """
    return int(string_in_list[0])

def mwm_results(results):
    return [unwrap(e['minwordsmatched']) for e in results['result']]
    
def wc_results(results):
    return unwrap(results['querywords'])
