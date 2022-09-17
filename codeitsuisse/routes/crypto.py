import logging
import json

from flask import request, Response

from codeitsuisse import app

logger = logging.getLogger(__name__)
memo_dict = {1 : 4, 2 : 4 , 4 : 4}


@app.route('/cryptocollapz', methods=['POST'])
def evaluate_crypto():
    data = request.get_json()
    final_output = []
    output = []

    for data_list in data:
        for elem in data_list:
            if elem not in memo_dict:
                crypto(elem)
            output.append(memo_dict[elem])
        final_output.append(output)
        output = []
    return Response(json.dumps(final_output), mimetype='application/json')


def collatz(number):
    if number % 2 == 0:
        return number // 2
    else:
        return (3 * number) + 1

def crypto(n):
    if n in memo_dict:
        return memo_dict[n]
    else:
        crypto(collatz(n))
        memo_dict[n] = max(n, memo_dict[collatz(n)])
