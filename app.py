from flask import Flask, Response, request, jsonify
from bson import Binary, Code
from bson.json_util import dumps
from pymongo import MongoClient
import re

app = Flask(__name__)

client = MongoClient()
db = client.condatos

def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    if request.method == 'OPTIONS':
        response.headers['Access-Control-Allow-Methods'] = 'DELETE, GET, POST, PUT'
        headers = request.headers.get('Access-Control-Request-Headers')
        if headers:
            response.headers['Access-Control-Allow-Headers'] = headers
    return response
app.after_request(add_cors_headers)


@app.route('/tweets', methods=['GET'])
def tweets():
    q = request.args.get('q')
    if q is None:
        data = list(db.tweets.find({}))
    else:
        term_list = q.split(" ")
        regexp = re.compile(r"|".join(term_list), re.IGNORECASE)
        data = list((db.tweets.find({"text":regexp})))
    return Response(dumps(data), mimetype='application/json')


if __name__ == '__main__':
    app.after_request(add_cors_headers)
    app.run(threaded=True, host='0.0.0.0', port=7001, debug=True)
