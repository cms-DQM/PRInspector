from flask import Flask, render_template
from views.prs import *
from datetime import datetime
import time

app = Flask(__name__,
            static_folder="./templates/static",
            template_folder="./templates")

@app.route('/')
def index():
    return get_prs_view()

@app.template_filter('datetime')
def format_date(date_string):
    def utc2local (utc):
        epoch = time.mktime(utc.timetuple())
        offset = datetime.fromtimestamp (epoch) - datetime.utcfromtimestamp (epoch)
        return utc + offset
    
    date = datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%SZ")
    date = utc2local(date)
    return date.strftime("%Y-%m-%d %H:%M:%S")

def run_flask():
    app.run(host='0.0.0.0',
            port=8080,
            debug=True,
            threaded=True)

if __name__ == '__main__':
    run_flask()