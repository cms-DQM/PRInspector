REPOSITORY = 'cms-sw/cmssw'

CERN_SSO_CERT_FILE = 'private/cert.pem'
CERN_SSO_KEY_FILE = 'private/cert.key'
CERN_SSO_COOKIES_LOCATION = 'private/'

TWIKI_CONTACTS_URL = 'https://threus.web.cern.ch/threus/ppd/ppd_contacts'
TWIKI_TAG_COLLECTOR_URL = 'https://twiki.cern.ch/twiki/bin/edit/CMS/DQMP5TagCollector?nowysiwyg=1'

def get_repo_url():
    return 'https://github.com/' + REPOSITORY + '/'

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
            'jet'
            ]
