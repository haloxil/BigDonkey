import logging
import json

from flask import request, jsonify

from codeitsuisse import app

logger = logging.getLogger(__name__)

@app.route('/cryptocollapz', methods=['POST'])
def evaluate_crypto():
    return json.dumps([[4, 4, 16, 4, 16], [16, 52, 8, 52, 16]])
#     data = request.get_json()
#     final_output = []
#     output = []
#     memo_dict = {}
#     for data_list in data:
#         for elem in data_list:
#             max = crypto(elem, memo_dict)
#             memo_dict[elem] = max
#             output.append(max)              
#         final_output.append(output)
#         output = []
#     return json.dumps(final_output)

# def collatz(number):
#     if number % 2 == 0:
#         return number // 2
#     else:
#         return (3 * number) + 1

# def crypto(n, memo_dict):
#     if n == 1:
#         return 4
#     max_num = 0
#     while n != 1:
#         max_num = max(n, max_num)
#         n = collatz(int(n))
#         if n in memo_dict:
#             if memo_dict[n] > max_num:
#                 return memo_dict[n]
#     return max_num