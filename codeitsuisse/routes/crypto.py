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
                max = num
                while (elem > 0):
                    if num % 2 == 0:
                        num /= 2
                    else:
                        num = num * 3 + 1
                    elem -= 1

                    if num > max:
                        max = num

                output.append(int(max))
                
        final_output.append(output)
        output = []
    return json.dumps(final_output)
    