import urllib.request
import json

def get_prs():
    response = urllib.request.urlopen("https://api.github.com/search/issues?q=repo:cms-sw/cmssw+is:pr+state:open+label:dqm-pending").read()
    content = json.loads(response)
    pending = content['items']

    response = urllib.request.urlopen("https://api.github.com/search/issues?q=repo:cms-sw/cmssw+is:pr+state:open+label:dqm-rejected").read()
    content = json.loads(response)
    rejected = content['items']

    return pending + rejected
