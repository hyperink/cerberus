#!/usr/bin/python
# -*- coding: utf-8 -*-
import web
import os
import google
import gdata
import json
import check
import shelve
from contextlib import closing

from localconf import mpdb
from localconf import PRINT_EBOOK_TOKEN
from localconf import DEFAULT

from hyperink_stdlib.api.v1.product import Product
from hyperink_stdlib.api.v1.book import Book
from hyperink_stdlib.api.v1.book import Content
from hyperink_stdlib.api.v1.imprint import Imprint
from hyperink_stdlib.api.v1.contributor import Contributor
from hyperink_stdlib.cloud import cloud_api as clapi
app_path = os.path.dirname(__file__)
SHELVE_NAME = 'last_thing'

urls = (
    "/?", "Index",                        # Michael's main interface
    "/summary/([0-9]+)/?", "MassRank",    # Get the summary for a single book
    "/summary/?", "MassRank",             # Mek's interface to show sorted book results summary
    "/listplace/?", "List",               # Google Docs Listing
    "/list/?", "ListJson",                # Google Docs Listing as JSON
    "/check/?", "Check",                  # Actual API call to 
    "/copywrong/([0-9]+)/?", "Copywrong", # Mek's wrapper to access SINGLE cached (wpid)
    "/copywrong/?", "Copywrong",          # Mek's wrapper to access all cached (wpids)
)

app = web.application(urls, globals())
render = web.template.render(app_path + '/templates/', base="layout")

class MassRank:
    def GET(self, wpid=all):
        if wpid is all:
            summary = sorted(json.loads(Copywrong().GET()), key=lambda x: x['score'])
            return render.summary(summary)
        else:
            return render.single_summary(json.loads(Copywrong().GET(wpid, details=True))[0])

class Copywrong:
    def GET(self, wpid=all, details=False):
        """
        Mek's Check API wrapper to check couchdb for cached Copyscape API calls.

        if all wpids, loops over all of the wpids on the hyperink.com
        live marketplace, else, it pulls a single wpid from the live
        marketplace. 

        NOTES:
        Stephen is doing some kind of interesting cacheing as well
        (see SHELVE_NAME and log), however, I'm not exactly sure how
        complete this is. I advise using couchdb for now.

        TODO:
        0. Copyscape failed due to insufficient credits
        1. prune any entry in couchdb ('copywrong_cache') with empty value {}      
        2. Calculate a score for the couchdb entry
        3. I've created new db ('copywrong_summary_cache)' for cacheing
           summaries {"score":, "title":} of API calls in a new couchdb table for fast lookup.
           
           You can see how to add entries by looking at ~/Publisure/apps/copywrong.py

        """
        i = web.input(data=None)
        if wpid is all:
            books = Book.get_all(db=mpdb)
        else:
            try:
                book = Book(wpid, db=mpdb)
                books = [book]
            except:
                return json.dumps({"error": "Invalid wpid"})

        url = "http://www.hyperinkpress.com/%s/print-ebook.php?token=" + PRINT_EBOOK_TOKEN
        sources = [{"wpid": b.wpid, "title": b.title,
                    "slug": b.slug, "url": url % (b.slug)} for b in books]
        results = []
        for src in sources:
            if clapi.exists('copywrong_cache', str(src['wpid'])):
                print("Pulling book wpid:%s from couchdb cache..." % src['wpid'])
                data = clapi.get('copywrong_cache', str(src['wpid']))
               
                try:
                    result = {"score": data['metric'],
                              "wpid": str(src['wpid']),
                              "title": src['title'],
                              "slug": src['slug']
                              }
                    
                    # Send result to couchdb cache:
                    if not clapi.exists('copywrong_summary_cache', str(src['wpid'])):
                        clapi.add('copywrong_summary_cache', str(src['wpid']), result)
                    if i.data or details:
                        result['data'] = data
                    results.append(result)
                except:
                    pass
            else:
                results.append({"error": "Entry not in couchdb",
                                "wpid": src['wpid'],
                                "title": src['title'],
                                "score": None,
                                "data": None,
                                "slug": src['slug'],
                                })
        return json.dumps(results)

class Index:
    def GET(self):
        return render.index()

class ListJson:
    """ Returns a list of gdoc files as JSON. See List below """
    def POST(self):
        email, password = get_email_password()
        try:
            return json.dumps(google.list_files(email, password), indent=4)
        except gdata.client.BadAuthentication as e:
            raise web.seeother("/?msg=Invalid+Email+or+Password")

class List:
    def POST(self):
        """
        Upon POST of your google email and password, List.POST() will
        return an html template containing a list of google documents
        """
        email, password = get_email_password()
        try:
            dlist = google.list_files(email, password)
            return render.list(email=email, password=password, dlist=dlist)
        except gdata.client.BadAuthentication as e:
            raise web.seeother("/?msg=Invalid+Email+or+Password")

class Check:
    """
    This is the entry point for calling the Ceberus Copyscape
    API. Client POSTS their document information to Check.POST()

    Either takes a google document, etc or a url
   
    """
    def GET(self):
        return self.POST()

    def POST(self):
        i = web.input(dtype='document', did=None, url=None, clean=False, test=0)
        did = i.did # google document_id
        dtype = i.dtype # google document type
        url = i.url
        test = bool(int(i.test))        

        if url:
            if test:
                return get_last()
            else:
                content = check.get_content(url, clean=i.clean)
                return content
                last = json.dumps(check.score(url, content), indent=4)
        else:
            email, password = get_email_password()
            if not (did and dtype):
                raise web.seeother("/?msg=Invalid+Id+or+Type")
            # {"metric": score, "data": {}}
            last = json.dumps(google.score(email, password, dtype, did), indent=4)
        log_last(last)
        return last

def get_email_password():
    i = web.input(email=None, password=None)
    if not (i.email and i.password):
        raise web.seeother("/?msg=Not+Authorized")
    else:
        return i.email, i.password

def log_last(last, shelve_name=SHELVE_NAME):
    with closing(shelve.open(shelve_name)) as s:
        s['last'] = last
    return last

def get_last(shelve_name=SHELVE_NAME):
    with closing(shelve.open(shelve_name)) as s:
        if 'last' in s:
            return s['last']
        else:
            return DEFAULT

if __name__ == "__main__":
    app.run()
