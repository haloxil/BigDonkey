# import logging
# import json
# import queue
# import heapq
# import math
# import pyjson5

# from flask import request, Response

# from codeitsuisse import app

# logger = logging.getLogger(__name__)
# @app.route('/hello', methods=['GET'])
# def default_routeStig():
#     return "Hello Template"

# @app.route('/stig/warmup', methods=['POST'])
# def stig_warmup():
#     data = pyjson5.decode(request.get_data(as_text=True))
#     output = []
#     for i in range(len(data)):
#         output.append(stig_warmup_logic(data[i]))
#     return Response(json.dumps(output),mimetype='application/json')


# def stig_warmup_logic(interview):
#     max = interview["maxRating"]
#     questions = interview["questions"]
#     total_values = {i for i in range(1,max+1)}
#     p=0
#     q=0
#     for real_value in range(1,max+1):
#         possible_values = total_values.copy()
#         for i in range(len(questions)):
#             question_values = {i for i in range(interview["questions"][i]["lower"],interview["questions"][i]["upper"]+1)}
#             if real_value in question_values:
#                 possible_values = possible_values.difference(total_values.difference(question_values))
#             else:
#                 possible_values = possible_values.difference(question_values)
#         if len(possible_values) == 1 and real_value in possible_values:
#             p += 1
#         elif min(possible_values) == real_value:
#             p += 1
#     gcd = math.gcd(p,max)
#     return {"p": int(p / gcd), "q": int(max / gcd)}

# @app.route('/stig/full', methods=['POST'])
# def stig_full():
#     output = []
#     return Response(json.dumps(output), mimetype='application/json')
