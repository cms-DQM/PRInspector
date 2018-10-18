from services.cern_sso_service import cert_sign_on
import hashlib
import requests
import pickle
import config

def get_contacts_list_html():
    cookies = __get_and_save_cookies(config.TWIKI_CONTACTS_URL)
    return requests.get(config.TWIKI_CONTACTS_URL, cookies=cookies).text

def get_author_mentioned_info(author, html):
    # TODO improve logic
    if author in html:
        return { 'text': 'Author is known', 'class': 'text-success' }
    else:
        return { 'text': 'Author is unknown', 'class': 'text-danger' }

def __get_and_save_cookies(url):
    hash = hashlib.md5(url.encode()).hexdigest()
    file = config.CERN_SSO_COOKIES_LOCATION + hash + '_cookies.p'

    try:
        cookies = pickle.load(open(file, 'rb'))
    except:
        cookies = cert_sign_on(url, cert_file=config.CERN_SSO_CERT_FILE, key_file=config.CERN_SSO_KEY_FILE, cookiejar=None)
        pickle.dump(cookies, open(file, 'wb'))

    return cookies
