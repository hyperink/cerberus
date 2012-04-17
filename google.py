#!/usr/bin/python
# -*- coding: utf-8 -*-
import web
import check
import gdata
import gdata.gauth
import gdata.auth
import gdata.docs
import gdata.docs.service
import gdata.docs.client

def gtype_gid_list():
    return gid_list

def get_gdoc_list():
    pass

class GoogleDocs:
    def GET(self, raw_feed=True, token_in_path=None):
        """
        Create a client class which will make HTTP requests with
        Google Docs server and then fetch a list of documents.

        """
        try:
            return list_entries()
        except Exception as e:
            if 'invalid token' in str(e).lower():
                return '<a href="%s">Login to your Google account</a>' % GetAuthSubUrl()
            raise e

def list_entries(raw_feed=False, token_in_path=None):
    url = web.ctx.homedomain
    if token_in_path:
        url += token_in_path
    else:
        url += web.ctx.fullpath
        
    single_use_token = gdata.auth.extract_auth_sub_token_from_url(url)
    client2 = gdata.docs.service.DocsService()
    client2.ssl = True
    client2.UpgradeToSessionToken(single_use_token)
    token_info = colient2.AuthSubTokenInfo()
    documents_feed = client2.GetDocumentListFeed()
    
    if raw_feed:
        return documents_feed.entry
    return content_feed(client2, documents_feed, limit=1)

def content_feed(client, documents_feed, limit=1):
    # a function with the client as a closure variable
    content_type_id = content_type_id_client(client) 
    return [content_type_id(dtype, did) for dtype, did in type_id_feed(documents_feed)[:limit]]

def type_id_feed(documents_feed):
    return [ds.resourceId.text.split(':') for ds in documents_feed.entry]

def content_type_id_client(client):
    def content_type_id_fn(dtype, did, limit=1):
        return clean_full_document(client, dtype, did)
    return content_type_id_fn

def get_service(email, password):
    client = gdata.docs.service.DocsService()
    client.ssl = True
    client.ClientLogin(email, password, 'arbitrary')
    return client

def get_client(email, password):
    client = gdata.docs.client.DocsClient()
    client.ssl = True
    client.ClientLogin(email, password, 'arbitrary')
    return client

def list_files(email, password):
    return display_feed(getfeed(email, password))

def getfeed(email, password):
    client = get_service(email, password)
    documents_feed = client.GetDocumentListFeed()
    return documents_feed

def display_feed(documents_feed):
    return tuple_to_dict([ds.resourceId.text.split(':') + [ds.title.text] for ds in documents_feed.entry])

def dictify(dtype, did, dtitle):
    return {
        "type": dtype,
        "id": did,
        "title": dtitle
    }

def score(email, password, dtype, did):
    content = get_content(email, password, dtype, did)
    xml = check.xml_from_content(content)
    dictd = check.dict_from_xml(xml)
    metric = check.metric_dict(dictd)
    return {"metric": metric, "data": dictd }

def tuple_to_dict(dlist):
    """
    dtype, did, dtitle -> {}
    """
    return [dictify(dtype, did, dtitle) for dtype, did, dtitle in dlist]
    
def get_content(email, password, doc_type, doc_id):
    """
    email, password, doc_type, doc_id -> content
    """
    return filegetter(email, password)(doc_type, doc_id)

def filegetter(email, password):
    """
    Returns a 'logged in' file getter that takes a doc_type and doc_id and returns the content of the file
    """
    client = get_client(email, password)
    def filegetter(doc_type, doc_id):
        return client.get_file_content('https://docs.google.com/feeds/download/%ss/Export?id=%s&format=txt' % (doc_type, doc_id))
    return filegetter

def GetAuthSubUrl():
  next = web.ctx.homedomain + "/"
  scopes = ['http://docs.google.com/feeds/', 'https://docs.google.com/feeds/']
  secure = False  # set secure=True to request a secure AuthSub token
  session = True
  return gdata.gauth.generate_auth_sub_url(next, scopes, secure=secure, session=session)

def clean_full_document(client, doc_type, doc_id, blog_path="imgstaging", preview=True):
    """
    Returns a Google Doc with 'clean' HTML.

    usage:
        >>> clean_full_document('document', doc_id)

    """
    return client.get_file_content('https://docs.google.com/feeds/download/%ss/Export?id=%s&format=text' % (doc_type, doc_id))
