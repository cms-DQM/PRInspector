from services.cern_sso_service import cert_sign_on
import hashlib
import requests
import pickle
import config
import re

def get_contacts_list_html():
    return requests.get(config.TWIKI_CONTACTS_URL).text

def get_tag_collector_html():
    cookies = __get_and_save_cookies(config.TWIKI_TAG_COLLECTOR_URL)
    text = requests.get(config.TWIKI_TAG_COLLECTOR_URL, cookies=cookies).text

    # Cancel editing so other people can access the edit page
    requests.post(config.TWIKI_TAG_COLLECTOR_CANCEL_EDIT_URL, cookies=cookies, data = {'action_cancel': 'Cancel'})

    if ('action="https://twiki.cern.ch/Shibboleth.sso/ADFS"' in text or 
        'document.forms[0].submit()' in text or 
        'Sign in with your CERN account' in text):
        cookies = __get_and_save_cookies(config.TWIKI_TAG_COLLECTOR_URL, True)
        text = requests.get(config.TWIKI_TAG_COLLECTOR_URL, cookies=cookies).text

    text = text.replace('&#42;', '*')
    text = text.replace('&#37;', '%')
    text = text.replace('&#91;', '[')
    
    return text

def get_author_mentioned_info(author, html):
    git_user_str = 'Git: [[https://github.com/%s][%s]]'%(author, author)
    if git_user_str in html:
        return { 'text': 'Author is known', 'class': 'text-success', 'description': "Author's Github username is mentioned in DQM Contacts Twiki page" }
    elif author in html:
        return { 'text': 'Author is mentioned', 'class': 'text-warning', 'description': "Author's Github username appears in DQM Contacts Twiki page, but it wasn't entered deliberately. This might be a coinsidence" }
    else:
        return { 'text': 'Author is unknown', 'class': 'text-danger', 'description': "Author's Github username doesn't appear in DQM Contacts Twiki page" }

def get_tag_collector_info(pr_number, html):
    print(html)
    regex_ok = r'%OK%([^%\n]*?)\]\[PR ' + str(pr_number) + r'\]\]'
    m_ok = re.compile(regex_ok)

    regex_prod = r'%PROD%([^%\n]*?)\]\[PR ' + str(pr_number) + r'\]\]'
    m_prod = re.compile(regex_prod)

    regex_notok = r'%NOTOK%([^%\n]*?)\]\[PR ' + str(pr_number) + r'\]\]'
    m_notok = re.compile(regex_notok)

    regex_mentioned = r'\*([^%\n]*?)\]\[PR ' + str(pr_number) + r'\]\]'
    m_mentioned = re.compile(regex_mentioned)

    if m_ok.search(html) or m_prod.search(html):
        return { 'tested': True, 'text': 'Tested in Playback', 'class': 'text-success', 'description': "This PR was tested in playback system and tests passed" }
    elif m_notok.search(html):
        return { 'tested': False, 'text': 'Rejected in Playback', 'class': 'text-danger', 'description': "This PR was tested and rejected in playback system" }
    elif m_mentioned.search(html):
        return { 'tested': False, 'text': 'Mentioned in Playback', 'class': 'text-warning', 'description': "This PR is mentioned in the playback system but it is not yet tested" }
    else:
        return { 'tested': False, 'text': 'Not mentioned in Playback', 'class': 'text-secondary', 'description': "This PR was does not appear in Tag Collector page" }

def __get_and_save_cookies(url, force_reload=False):
    hash = hashlib.md5(url.encode()).hexdigest()
    file = config.CERN_SSO_COOKIES_LOCATION + hash + '_cookies.p'

    cookies = None

    if not force_reload:
        try:
            cookies = pickle.load(open(file, 'rb'))
        except:
            pass
    
    if cookies == None:
        cookies = cert_sign_on(url, cert_file=config.CERN_SSO_CERT_FILE, key_file=config.CERN_SSO_KEY_FILE, cookiejar=None)
        pickle.dump(cookies, open(file, 'wb'))
    
    return cookies

