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
    response = urllib.request.urlopen(__add_token('https://api.github.com/search/issues?q=repo:cms-sw/cmssw+is:pr+state:open+label:dqm-pending', access_token)).read()
    content = json.loads(response)
    pending = content['items']
    
    response = urllib.request.urlopen(__add_token('https://api.github.com/search/issues?q=repo:cms-sw/cmssw+is:pr+state:open+label:dqm-rejected', access_token)).read()
    content = json.loads(response)
    rejected = content['items']

    return pending + rejected

def __add_token(url, access_token):
    if access_token != None and access_token != '':
        return url + '&access_token=' + access_token
    else:
        return url
