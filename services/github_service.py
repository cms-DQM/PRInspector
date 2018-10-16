from services.text_enrichment_service import enrich_comment
import datetime
import urllib.request
import urllib.parse
import json

def exchange_code_to_token(code):
    if code == None or code == '':
        return None
    
    try:
        data = {'client_id': '90704daa46bd69de5beb', 'client_secret': '54b4ed1ffecb539996bdee620fc963040cb14cda', 'code': code}
        req = urllib.request.Request('https://github.com/login/oauth/access_token', urllib.parse.urlencode(data).encode('utf-8'))
        req.add_header('Accept', 'application/json')
        response = urllib.request.urlopen(req).read()
        content = json.loads(response)
        return content['access_token']
    except Exception as e:
        print(e)
        return None

def get_prs(access_token=None):
    url = __add_token('https://api.github.com/search/issues?q=repo:cms-sw/cmssw+is:pr+state:open+label:dqm-pending', access_token)
    response = urllib.request.urlopen(url).read()
    content = json.loads(response)
    pending = content['items']
    
    url = __add_token('https://api.github.com/search/issues?q=repo:cms-sw/cmssw+is:pr+state:open+label:dqm-rejected', access_token)
    response = urllib.request.urlopen(url).read()
    content = json.loads(response)
    rejected = content['items']

    prs = pending + rejected
    for pr in prs:
        pr['body'] = enrich_comment(pr['body'])

    return prs

def get_last_comment(url, updated_at, access_token=None):
    since = datetime.datetime.strptime(updated_at, "%Y-%m-%dT%H:%M:%SZ")
    since -= datetime.timedelta(minutes=30)
    since = since.strftime("%Y-%m-%dT%H:%M:%SZ")
    
    url = __add_token(url + '?since=' + since, access_token)
    response = urllib.request.urlopen(url).read()

    content = json.loads(response)
    
    if len(content) > 0:
        return content[-1]
    else:
        return None

# TODO: Remove this
def get_test():
    url = 'https://twiki.cern.ch/twiki/bin/viewauth/CMS/DQMContacts'
    req = urllib.request.Request(url)
    req.add_header('Cookie', '_shibsession_64656661756c7468747470733a2f2f73686962342e6365726e2e63682f53686962626f6c6574682e73736f2f41444653=_59d5aa4ae6cdf757e09e31a7eef90ecc')
    return urllib.request.urlopen(req).read()

def __add_token(url, access_token):
    if access_token != None and access_token != '':
        return url + '&access_token=' + access_token
    else:
        return url
