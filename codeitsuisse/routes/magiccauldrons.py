import logging
import json
import queue
import heapq

from flask import request, jsonify

from codeitsuisse import app

logger = logging.getLogger(__name__)
@app.route('/hello', methods=['GET'])
def default_routeCauldron():
    return "Hello Template"

@app.route('/magiccauldrons', methods=['POST'])
def cauldron():
    data = request.get_json()
    num_cases = len(data)
    output = []
    for i in range(num_cases):
        output.append(cauldron_logic(data[i]))
    return json.dumps(output)

def cauldron_logic(stream: list):
    output_dict = {}
    store = [[-1] * (i+1) for i in range(stream["part1"]["row_number"]+1)]
    def get_water(row,col,initial_water):
        if(col < 0 or col > row): return 100
        if(store[row][col] != -1): return store[row][col]
        if(row == 0): return initial_water
        store[row][col] = (get_water(row-1,col-1,initial_water)-100 + get_water(row-1,col,initial_water)-100)/2.0
        return store[row][col]
    def bin_search(stream):
        nonlocal store
        lo = 0
        hi = (stream["part2"]["row_number"]**2 + 1) * (100 / stream["part2"]["flow_rate"])
        while hi - lo > 1:
            store = [[-1] * (i+1) for i in range(stream["part2"]["row_number"]+1)]
            mid = (hi + lo) // 2
            if(get_water(stream["part2"]["row_number"],stream["part2"]["col_number"],stream["part2"]["flow_rate"]*mid)) < stream["part2"]["amount_of_soup"]:
                lo = mid + 1
            else: hi = mid
        if (get_water(stream["part2"]["row_number"],stream["part2"]["col_number"],stream["part2"]["flow_rate"]*lo) == stream["part2"]["amount_of_soup"]):
            return lo
        elif (get_water(stream["part2"]["row_number"],stream["part2"]["col_number"],stream["part2"]["flow_rate"]*hi) == stream["part2"]["amount_of_soup"]):
            return hi
        else: print("could not find possible timing!!!")
    def get_water_lopsided(row,col,initial_water):
        if(col < 0 or col>row): return 150.0 if(col%2 == 0) else 100.0
        if(store[row][col] != -1): return store[row][col]
        if(row == 0): return initial_water
        store[row][col] = (get_water_lopsided(row-1,col-1,initial_water)-(100.0 if col%2 == 0 else 150.0) + get_water_lopsided(row-1,col,initial_water)-(150.0 if col%2 == 0 else 100.0))/2.0
        return store[row][col]
    def bin_search_lopsided(stream):
        nonlocal store
        lo = 0
        hi = (stream["part4"]["row_number"]**2 + 1) * (100.0 / stream["part4"]["flow_rate"])
        while hi - lo > 1:
            store = [[-1] * (i+1) for i in range(stream["part4"]["row_number"]+1)]
            mid = (hi + lo) // 2
            res = get_water_lopsided(stream["part4"]["row_number"],stream["part4"]["col_number"],stream["part4"]["flow_rate"]*mid)
            if res < stream["part4"]["amount_of_soup"]:
                lo = mid + 1
            else: hi = mid
        if (get_water_lopsided(stream["part4"]["row_number"],stream["part4"]["col_number"],stream["part4"]["flow_rate"]*lo) == stream["part4"]["amount_of_soup"]):
            return lo
        elif (get_water_lopsided(stream["part4"]["row_number"],stream["part4"]["col_number"],stream["part4"]["flow_rate"]*hi) == stream["part4"]["amount_of_soup"]):
            return hi
        else: return hi

    part1raw = 1.0*(get_water(stream["part1"]["row_number"],stream["part1"]["col_number"],stream["part1"]["flow_rate"]*stream["part1"]["time"]))
    output_dict["part1"] = min(part1raw,100.0)
    store = [[-1] * (i+1) for i in range(stream["part2"]["row_number"]+1)]
    output_dict["part2"] = round(bin_search(stream))
    store = [[-1] * (i+1) for i in range(stream["part3"]["row_number"]+1)]
    part3raw = 1.0*(get_water_lopsided(stream["part3"]["row_number"],stream["part3"]["col_number"],stream["part3"]["flow_rate"]*stream["part3"]["time"]))
    output_dict["part3"] = min(part3raw,150.0) if stream["part3"]["col_number"]%2 == 0 else min(part3raw,100.0)
    store = [[-1] * (i+1) for i in range(stream["part4"]["row_number"]+1)]
    output_dict["part4"] = round(bin_search_lopsided(stream))
    return output_dict


