from services.text_enrichment_service import enrich_comment
import config
import datetime
import urllib.request
import urllib.parse
import json
import re

def exchange_code_to_token(code):
    if code == None or code == '':
        return None
    
    try:
        data = {'client_id': config.get_github_client_id(), 'client_secret': config.get_github_client_secret(), 'code': code}
        req = urllib.request.Request('https://github.com/login/oauth/access_token', urllib.parse.urlencode(data).encode('utf-8'))
        req.add_header('Accept', 'application/json')
        response = urllib.request.urlopen(req).read()
        content = json.loads(response)
        return content['access_token']
    except Exception as e:
        print(e)
        return None

def get_not_merged_prs_count(access_token=None):
    req = urllib.request.Request('https://api.github.com/search/issues?q=repo:cms-sw/cmssw+is:pr+state:open+label:dqm-approved')
    __add_token(req, access_token)
    response = urllib.request.urlopen(req).read()
    content = json.loads(response)
    return content['total_count']

def get_prs(access_token=None):
    req = urllib.request.Request('https://api.github.com/search/issues?q=repo:cms-sw/cmssw+is:pr+state:open+label:dqm-pending')
    __add_token(req, access_token)
    response = urllib.request.urlopen(req).read()
    content = json.loads(response)
    pending = content['items']
    
    req = urllib.request.Request('https://api.github.com/search/issues?q=repo:cms-sw/cmssw+is:pr+state:open+label:dqm-rejected')
    __add_token(req, access_token)
    response = urllib.request.urlopen(req).read()
    content = json.loads(response)
    rejected = content['items']

    prs = pending + rejected
    for pr in prs:
        pr['body'] = enrich_comment(pr['body'])
    
    return prs

def get_merged_prs(access_token=None):
    req = urllib.request.Request('https://api.github.com/search/issues?q=repo:cms-sw/cmssw+is:pr+is:merged+label:dqm-pending+created:>2018-06-01')
    __add_token(req, access_token)
    response = urllib.request.urlopen(req).read()
    content = json.loads(response)
    merged_pending = content['items']

    for pr in merged_pending:
        pr['body'] = enrich_comment(pr['body'])
    
    return merged_pending

def get_last_comment(url, updated_at, access_token=None):
    since = datetime.datetime.strptime(updated_at, "%Y-%m-%dT%H:%M:%SZ")
    since -= datetime.timedelta(minutes=30)
    since = since.strftime("%Y-%m-%dT%H:%M:%SZ")
    
    req = urllib.request.Request(url + '?since=' + since)
    __add_token(req, access_token)
    response = urllib.request.urlopen(req).read()

    content = json.loads(response)
    
    if len(content) > 0:
        return content[-1]
    else:
        return None

def get_issues(access_token=None):
    req = urllib.request.Request('https://api.github.com/search/issues?q=repo:cms-sw/cmssw+is:issue+state:open+label:dqm-pending')
    __add_token(req, access_token)
    response = urllib.request.urlopen(req).read()
    content = json.loads(response)
    issues = content['items']

    for issue in issues:
        issue['body'] = enrich_comment(issue['body'])
    
    return issues

def get_dqm_categories():
    response = urllib.request.urlopen(config.CATEGORIES_MAP_URL).read()
    response = response.decode('utf-8')

    begin_index = response.find('"dqm": [') + 8
    end_index = response.find('],', begin_index)
    
    result = response[begin_index + 1:end_index]
    
    categories = result.split(',')
    categories = [item.strip('\n').strip(' ').strip('"') for item in categories]
    categories = filter(None, categories)
    
    categories = [item for item in categories if item.startswith('DQM/') == False]
    categories.append('DQM/*')

    categories = [item for item in categories if item.startswith('DQMOffline/') == False]
    categories.append('DQMOffline/*')

    categories = [item for item in categories if item.startswith('DQMServices/') == False]
    categories.append('DQMServices/*')

    categories = [item for item in categories if item.startswith('Validation/') == False]
    categories.append('Validation/*')

    return categories

def __add_token(req, access_token):
    if access_token != None and access_token != '':
        req.add_header('Authorization', 'token %s' % access_token)
