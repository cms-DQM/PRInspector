from flask import make_response, redirect

def github_logout():
    resp = make_response(redirect('/'))
    resp.delete_cookie('access_token')
    return resp
