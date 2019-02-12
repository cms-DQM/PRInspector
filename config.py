IS_TEST = True

REPOSITORY = 'cms-sw/cmssw'

def get_repo_url():
    return 'https://github.com/' + REPOSITORY + '/'

CERN_SSO_CERT_FILE = 'private/cert.pem'
CERN_SSO_KEY_FILE = 'private/cert.key'
CERN_SSO_COOKIES_LOCATION = 'private/'

TWIKI_CONTACTS_URL = 'https://ppdcontacts.web.cern.ch/PPDContacts/ppd_contacts'
TWIKI_TAG_COLLECTOR_URL = 'https://twiki.cern.ch/twiki/bin/edit/CMS/DQMP5TagCollector?nowysiwyg=1'
TWIKI_TAG_COLLECTOR_CANCEL_EDIT_URL = 'https://twiki.cern.ch/twiki/bin/save/CMS/DQMP5TagCollector'

TWIKI_TIMEOUT_SECONDS = 10

__github_client_id = None
__github_client_secret = None

def get_github_client_id():
    global __github_client_id
    if __github_client_id == None:
        __github_client_id = open('private/github_oauth_data.txt', 'r').readlines()[1].strip()
    return __github_client_id

def get_github_client_secret():
    global __github_client_secret
    if __github_client_secret == None:
        __github_client_secret = open('private/github_oauth_data.txt', 'r').readlines()[2].strip()
    return __github_client_secret

def get_subsystems():
    return ['l1t',
            'hlt',
            'tracker',
            'sistrip',
            'pixel',
            'ecal',
            'hcal',
            'dt',
            'rpc',
            'csc',
            'ct-pps',
            'ctpps',
            'bril',
            'gem',
            'hgcal',
            'tracking',
            'btag',
            'vertexing',
            'e-gamma',
            'jetmet',
            'lumi',
            'muon',
            'tau',
            'generators',
            'hfnose',
            'beamspot',
            'jme',
            'jet',
            'eventdisplay',
            'castor',
            'validation',
            ]
