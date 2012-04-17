#!/usr/bin/python
# -*- coding: utf-8 -*-
import web
import google
import gdata
import json

urls = (
    "/?", "Index",
    "/listplace/?", "List",
    "/list/?", "ListJson",
    "/check/?", "Check"
)

app = web.application(urls, globals())
render = web.template.render('templates', base="layout")

class Index:
    def GET(self):
        return render.index()

def get_email_password():
    i = web.input(email=None, password=None)
    if not (i.email and i.password):
        raise web.seeother("/?msg=Not+Authorized")
    else:
        return i.email, i.password

class ListJson:
    def POST(self):
        email, password = get_email_password()
        try:
            return json.dumps(google.list_files(email, password))
        except gdata.client.BadAuthentication as e:
            raise web.seeother("/?msg=Invalid+Email+or+Password")

class List:
    def POST(self):
        email, password = get_email_password()
        try:
            dlist = google.list_files(email, password)
            return render.list(email=email, password=password, dlist=dlist)
        except gdata.client.BadAuthentication as e:
            raise web.seeother("/?msg=Invalid+Email+or+Password")

class Check:
    def POST(self):
        email, password = get_email_password()
        i = web.input(dtype='document', did=None)
        did = i.did
        dtype = i.dtype
        if not (did and dtype):
            raise web.seeother("/?msg=Invalid+Id+or+Type")
        # {"metric": score, "data": {}}
        return json.dumps(google.score(email, password, dtype, did))

if __name__ == "__main__":
    app.run()
