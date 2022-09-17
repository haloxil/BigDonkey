import logging
import json
import demjson3
import queue
import heapq

from flask import request, Response

from codeitsuisse import app

logger = logging.getLogger(__name__)
@app.route('/hello', methods=['GET'])
def default_routeDNSCache():
    return "Hello Template"
table = {}
@app.route('/instantiateDNSLookup', methods=['POST'])
def instantiate_dnscache():
    global table
    data = demjson3.decode(request.get_data())
    table = data["lookupTable"]
    output = {"success": True}
    return Response(json.dumps(output),mimetype='application/json')

@app.route('/simulateQuery', methods=['POST'])
def query_dnscache():
    output = []
    global table
    data = demjson3.decode(request.get_data())
    cacheSize = data["cacheSize"]
    cache = []
    log = data["log"]
    for i in range(len(log)):
        if log[i] in cache:
            output.append({"status":'cache hit', "ipAddress": table[log[i]]})
            cache.remove(log[i])
            cache.append(log[i])
        elif log[i] in table:
            output.append({"status":'cache miss', "ipAddress": table[log[i]]})
            if len(cache) == cacheSize:
                cache.pop(0)
            cache.append(log[i])
        else: output.append({ "status": 'invalid', "ipAddress": None})

    return Response(json.dumps(output), mimetype='application/json')

def dnscache_logic(stream: list):
    return None


