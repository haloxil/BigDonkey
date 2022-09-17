import logging
import json

from flask import request, jsonify

from codeitsuisse import app

logger = logging.getLogger(__name__)

@app.route('/cryptocollapz', methods=['POST'])
def evaluate_crypto():
    data = request.get_json()
    final_output = []
    output = []
    for data_list in data:
        for elem in data_list:
            output.append(crypto(elem))              
        final_output.append(output)
        output = []
    return json.dumps(final_output)

def collatz(number):
    if number % 2 == 0:
        return number // 2
    else:
        return (3 * number) + 1

def crypto(n):
    max_num = 0
    while n != 1:
        max_num = max(n, max_num)
        n = collatz(int(n))
    return max_num