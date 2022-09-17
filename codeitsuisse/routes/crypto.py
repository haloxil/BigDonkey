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
            if (elem & (elem-1) == 0) and elem != 0:
                output.append(elem)
            else:   
                num = elem
                num_list = []
                while (elem > 0):
                    if num % 2 == 0:
                        num /= 2
                    else:
                        num = num * 3 + 1
                    elem -= 1

                    num_list.append(num)
                output.append(int(max(num_list)))
        final_output.append(output)
        output = []
    return json.dumps(final_output)
    