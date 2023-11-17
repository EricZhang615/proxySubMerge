from flask import Flask, send_file
import flask_restful as restful
from flask_restful import reqparse
from fetch import fetch_yml
from ymlMerge import load_yaml, merge_yaml, save_yaml
from subs import subs, token

app = Flask(__name__)
api = restful.Api(app)

parser = restful.reqparse.RequestParser()
parser.add_argument('token', type=str, location='args')

def fetch_and_merge():
    for sub in subs:
        fetch_yml(sub['url'], sub['name'])

    template = load_yaml('template.yml')
    sub1 = load_yaml(subs[0]['name']+'.yml')
    # sub2 = load_yaml(subs[1]['name']+'.yml')
    rules = load_yaml('rules.yml')
    merge_yaml(template, sub1, None, rules)
    save_yaml('merged.yml', template)

class SubsMerge(restful.Resource):
    def get(self):
        args = parser.parse_args()['token']
        if args != token:
            return 'Forbidden', 403
        else:
            fetch_and_merge()
        return send_file('merged.yml')


api.add_resource(SubsMerge, '/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)