from flask import Flask, make_response, render_template, request, redirect
from services.github_service import get_prs, get_last_comment, exchange_code_to_token
from services.pr_info_service import get_subsystem_in_title_info
from services.twiki_service import get_contacts_list_html, get_author_mentioned_info
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

    # Init key for additional properties
    for pr in prs:
        pr['additional'] = {}

    # Check if subsystem was mentioned in the title
    for pr in prs:
        pr['additional']['subsystem'] = get_subsystem_in_title_info(pr['title'])

    # Check if author is in contacts list
    contacts_html = get_contacts_list_html()
    for pr in prs:
        pr['additional']['author'] = get_author_mentioned_info(pr['user']['login'], contacts_html)
    
    # Get last comment
    # for pr in prs:
    #     pr['additional']['last_comment'] = { 'body': '...' }
        #pr['last_comment'] = get_last_comment(pr['comments_url'], pr['updated_at'], access_token)

    return make_response(render_template('index.html', prs=prs, access_token=access_token))
