from flask import Flask, render_template
from services.github_service import *
import urllib.request
import json

def get_prs_view():
    prs = get_prs()
    
    return render_template('index.html', prs=prs)
