import logging
import json
import numpy as np

from flask import request, Response

from codeitsuisse import app

logger = logging.getLogger(__name__)


@app.route('/rubiks', methods=['POST'])
def evaluate_rubiks():
    data = request.get_json()
    ops = data["ops"]
    state = data["state"]

    op = "U"
    if op == "U":
        state['u'] = (np.array(state['u']).transpose).tolist()

    print(ops)
    print(state)
    return json.dumps("hello")