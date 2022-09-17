import logging
import json

from flask import request, Response

from codeitsuisse import app

logger = logging.getLogger(__name__)


@app.route('/calendarDays', methods=['POST'])
def evaluate_calendar():
    data = request.get_json()
    numbers = data["numbers"]
    part1 = ""
    if (len(numbers) == 1):
        for i in range(9):
            part1 += 7*" " + ","

    output_dict = {"part1": [part1]}
    return json.dumps(output_dict)