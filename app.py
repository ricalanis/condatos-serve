from flask import Flask, Response, request, jsonify
import simplejson as json
from pymongo import MongoClient

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
        data = list((db.tweets.find({"text":q})))
    return Response(data, mimetype='application/json')


if __name__ == '__main__':
    app.after_request(add_cors_headers)
    app.run(threaded=True, host='0.0.0.0', port=9000, debug=True)
