from flask import Flask, render_template, request
from views.prs import get_prs_view
from datetime import datetime
import argparse
import time

app = Flask(__name__,
            static_folder="./templates/static",
            template_folder="./templates")

@app.route('/')
def index():
    code = request.args.get('code')
    return get_prs_view(code)

@app.template_filter('datetime')
def format_date(date_string):
    def utc2local (utc):
        epoch = time.mktime(utc.timetuple())
        offset = datetime.fromtimestamp (epoch) - datetime.utcfromtimestamp (epoch)
        return utc + offset
    
    date = datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%SZ")
    date = utc2local(date)
    return date.strftime("%Y-%m-%d %H:%M:%S")

def run_flask(debug=True):
    app.run(host='0.0.0.0',
            port=8080,
            debug=debug,
            threaded=True)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run the web app.')
    parser.add_argument('-d', dest='debug', action='store_true',
                    help='debug mode')
    args = parser.parse_args()

    run_flask(args.debug)
