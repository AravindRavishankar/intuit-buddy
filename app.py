#!/usr/bin/env python

from __future__ import print_function
from future.standard_library import install_aliases
install_aliases()

from urllib.parse import urlparse, urlencode
from urllib.request import urlopen, Request
from urllib.error import HTTPError

import json
import os

from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)
    print("Request1:")
    print(json.dumps(req, indent=4))
    print("1")
    res = processRequest(req)
    print(res)
    print("2")
    res = json.dumps(res, indent=4)
    print(res)
    # print(res)
    r = make_response(res)
    print(r)
    print("3")
    r.headers['Content-Type'] = 'application/json'
    print("4")
    return r


def processRequest(req):
    result = req.get("result")
    print("Result:")
    print(result)
    parameters = result.get("parameters")
    print(parameters)
    base_url = 'https://intuit.service-now.com/sp?id=search&t=&q='
    ln = len(parameters.values())
    ctr = 0
    for p in parameters.values():
        ctr += 1
        base_url += p
        if ctr != ln:
            base_url += '%20'
        else:
            base_url +='&search='
    #result = urlopen(base_url).read()
    #data = json.loads(base_url)
    res = makeWebhookResult(base_url)
    print(res)
    return res


def makeWebhookResult(data):
    return {
        "speech": data,
        "displayText": data,
        # "data": data,
        # "contextOut": [],
        "source": "buddy"
    }


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)

    app.run(debug=False, port=port, host='0.0.0.0')
