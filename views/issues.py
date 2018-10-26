from flask import Flask, make_response, render_template, request, redirect
from services.github_service import get_issues, exchange_code_to_token

def get_issues_view(code):
    if code != None and code != '':
        access_token = exchange_code_to_token(code)

        if access_token != None and access_token != '':
            # Save cookie and redirect user to issues page (without code parameter)
            resp = make_response(redirect('/issues'))
            resp.set_cookie('access_token', access_token)
            return resp
    else:
        access_token = request.cookies.get('access_token')

    issues = get_issues(access_token)

    # Init key for additional properties
    for issue in issues:
        issue['additional'] = {}

    # Set background color
    for issue in issues:
        issue['additional']['background'] = 'bg-white'

    return make_response(render_template('issues.html', 
                                         issues=issues, 
                                         access_token=access_token))
