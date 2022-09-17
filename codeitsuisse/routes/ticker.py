import logging
import json
import queue
import heapq

from flask import request, jsonify

from codeitsuisse import app

logger = logging.getLogger(__name__)
@app.route('/hello', methods=['GET'])
def default_route2():
    return "Hello Template"

@app.route('/tickerStreamPart1', methods=['POST'])
def to_cumulative1():
    data = request.get_json()
    stream = data["stream"]
    return to_cumulative_delayed(stream, 1)

@app.route('/tickerStreamPart2', methods=['POST'])
def to_cumulative2():
    data = request.get_json()
    stream = data["stream"]
    quantity_block = data["quantityBlock"]
    return to_cumulative_delayed(stream, quantity_block)


def to_cumulative_delayed(stream: list, quantity_block: int):  #Returns: ["timestamp,ticker1,quantity1,notional1,,ticker2,quantity2,notional2...",]
    def update_cum_dict():
        out = ""
        for ticker in cur_dict.keys():
            if cur_dict[ticker][0] < quantity_block:
                continue
            left = cur_dict[ticker][0] % quantity_block
            taken = cur_dict[ticker][0] - left
            if ticker in cum_dict:
                cum_dict[ticker][0] += taken
                cum_dict[ticker][1] += cur_dict[ticker][1] - left*cur_dict[ticker][2]
                cur_dict[ticker][1] -= cur_dict[ticker][1] - left*cur_dict[ticker][2]
                cur_dict[ticker][0] -= taken
            else:
                cum_dict[ticker] = [taken, cur_dict[ticker][1] - left*cur_dict[ticker][2]]
                cur_dict[ticker][1] -= cur_dict[ticker][1]  - left*cur_dict[ticker][2]
                cur_dict[ticker][0] -= taken
            out += "," + ticker + "," + str(cum_dict[ticker][0]) + "," + str(
                "{:.1f}".format(cum_dict[ticker][1]))
        return out

    timestamp_hq = list(map(lambda x: x.split(","), stream))
    heapq.heapify(timestamp_hq)
    output = []
    cum_dict = {
    }  #Format {ticker : [cum_quantity%quantity_block == 0, cum_notional]}
    cur_dict = {
    }  #Format {ticker : [quantity(< quantity_block), cum_notional, last_price]}
    current_timestamp = ""
    curr_out = ""
    while not len(timestamp_hq) == 0:

        item = heapq.heappop(timestamp_hq)

        if item[0] != current_timestamp:  #next timestamp
            curr_out += update_cum_dict()
            if not curr_out == "":
                output.append(current_timestamp + curr_out)
            current_timestamp = item[0]
            curr_out = ""

        if item[1] in cur_dict:
            cur_dict[item[1]][0] += int(item[2])
            cur_dict[item[1]][1] += float(item[2]) * float(item[3])
            cur_dict[item[1]][2] = float(item[3])
        else:
            cur_dict[item[1]] = [int(item[2]), float(item[2]) * float(item[3]), float(item[3])]
        curr_out += update_cum_dict()
    curr_out += update_cum_dict()
    if not curr_out == "":
        output.append(current_timestamp + curr_out)
    
    output_dict = {"output": output}
    return json.dumps(output_dict)