import logging
import json

from flask import request, Response

from codeitsuisse import app

logger = logging.getLogger(__name__)
memo_dict = {}


@app.route('/cryptocollapz', methods=['POST'])
def evaluate_crypto():
    data = request.get_json()
    final_output = []
    output = []
    return Response(json.dumps([[1,2,3,4],[5,6,7,8]]), mimetype='application/json')

    for data_list in data:
        for elem in data_list:
            max = crypto(elem)
            memo_dict[elem] = max
            output.append(max)
        final_output.append(output)
        output = []
    return Response(json.dumps([[1,2,3,4],[5,6,7,8]]), mimetype='application/json')

def collatz(number):
    if number % 2 == 0:
        return number // 2
    else:
        return (3 * number) + 1

def crypto(n):
    if n == 1:
        return 4
    max_num = 0
    while n != 1:
        max_num = max(n, max_num)
        n = collatz(int(n))
        if n in memo_dict:
            if memo_dict[n] > max_num:
                return memo_dict[n]
    return max_num
