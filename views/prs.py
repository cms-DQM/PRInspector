from flask import Flask, make_response, render_template, request, redirect
from services.github_service import get_prs, get_last_comment, exchange_code_to_token
import urllib.request
import json

def get_prs_view(code):
    if code != None and code != '':
        access_token = exchange_code_to_token(code)

        if access_token != None and access_token != '':
            # Save cookie and redirect user to main page (without code parameter)
            resp = make_response(redirect('/'))
            resp.set_cookie('access_token', access_token)
            return resp
    else:
        access_token = request.cookies.get('access_token')
    
    prs = get_prs(access_token)

    for pr in prs:
        pr['last_comment'] = get_last_comment(pr['comments_url'], pr['updated_at'], access_token)
    
    return make_response(render_template('index.html', prs=prs, access_token=access_token))
