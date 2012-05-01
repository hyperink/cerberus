#!/usr/bin/python
# -*- coding: utf-8 -*-
from contextlib import closing
import xml_utils
import re
import urllib
import urllib2
import requests
from hyperink_stdlib.utils.util import unhtml
from cStringIO import StringIO

DEFAULT_FILE = "examples/copyscape_example.xml"

def score(url, content=None):
    """
    """
    if not content:
        content = content_url(url) # get/read-in data of src url
    dictd = dict_from_xml(xml_from_content(content))
    metric = metric_dict(dictd)
    return { "metric": metric, "data": dictd }

def get_content(url, clean=False):
    """
    An extensible version of content_url()
    Consumes: url
    Returns: file content of url
    If the user wishes to run copyscape with a url, this url will be
    resolved and the file will be read in to memeory
    """
    with closing(urllib.urlopen(url)) as u:
        html = urllib.urlopen(url).read()
    if clean:
        return re.sub(' +', ' ', unicode(unhtml(html), errors="ignore").replace("\n", " "))
    return html

def content_url(url):
    """
    Consumes: url
    Returns: file content of url
    If the user wishes to run copyscape with a url, this url will be
    resolved and the file will be read in to memeory
    """
    with closing(urllib.urlopen(url)) as u:
        return u.read()

def xml_from_content(content):
    """ content -> xml """
    url = url_content(content)
    data = data_content(content)
    r = requests.post(url, data=data)
    return r.text

def dict_from_xml(xml):
    """
    converts xml -> dictionary
    """
    return xml_utils.xmltodict(xml.encode('utf-8'))

def metric_dict(dict_results):
    """ 
    results is a dict of the xml
    \Sigma_{i=0}^{n} 1/n^2 * mwf/wc
    """
    wc = wc_results(dict_results)
    mwm = mwm_results(dict_results)
    return sum(((n + 1)**-2 * mwf / wc for n, mwf in enumerate(mwm)))

def metric_content(content):
    """
    text -> metric
    """
    return metric_dict(dict_from_xml(xml_from_content(content)))


def test_xml(fn=DEFAULT_FILE):
    with closing(open(fn)) as f:
        return f.read()

def xml_from_url(url):
    """ url -> xml
    """
    return text_xml()

def file_content(content):
    return StringIO(content)

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

def metric_filename(filename):
    """
    File on disk -> metric
    """
    return metric_dict(dict_from_xml(xml_from_content(content_filename(filename))))

def unwrap(string_in_list):
    """ [u'26'] -> 26 """
    return int(string_in_list[0])

def mwm_results(results):
    return [unwrap(e['minwordsmatched']) for e in results['result']]
    
def wc_results(results):
    return unwrap(results['querywords'])
