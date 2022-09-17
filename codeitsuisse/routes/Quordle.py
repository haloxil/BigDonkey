from random import Random, random, randrange
import re

import logging
import json

from flask import request, Response
from codeitsuisse import app

ALPHABETS = {'A': 0, 'B': 0, 'C': 0, 'D': 0, 'E': 0, 'F': 0, 'G': 0, 'H': 0, 'I': 0, 'J': 0, 'K': 0, 'L': 0, 'M': 0,
             'N': 0, 'O': 0, 'P': 0, 'Q': 0, 'R': 0, 'S': 0, 'T': 0, 'U': 0, 'V': 0, 'W': 0, 'X': 0, 'Y': 0, 'Z': 0}


@app.route('/quordleKeyboard', methods=['POST'])
def evaluate_quordle():
    data = request.get_json()
    alphabet_data = dict(ALPHABETS)
    answers = data["answers"]
    attempts = data['attempts']
    numbers = data["numbers"]
    ans_data = dict(ALPHABETS)
    for x in answers:
        for letter in x:
            ans_data[letter] += 1

    answers_temp = answers.copy()
    for x in attempts:
        step(answers_temp, x, alphabet_data, ans_data)

    step1ans,leftovers = resolve(alphabet_data)
    step2ans = part2(step1ans, numbers) + leftovers

    return Response(json.dumps({"part1": step1ans, "part2": step2ans}), mimetype='application/json')


def step(ans, next_inp, data: dict, ans_data):

    if next_inp in ans:
        ans.remove(next_inp)
        for ltr in next_inp:
            ans_data[ltr] -= 1

    for letter in next_inp:
        if ans_data[letter] == 0 and data[letter] == 0:
            data[letter] = -1#flag to prevent doublecounting

    for x in data.keys():
        if data[x] > 0 and ans_data[x] == 0:
            data[x] += 1

        if data[x] == -1:
            data[x] = 1


def resolve(data: dict):
    output = ""
    leftovers = ""
    for x in sorted(data.keys()):
        output += str(data[x]) if data[x] > 0 else ""
        if data[x] == 0:
            leftovers += x
    return output,leftovers


def part2(inp_str, numbers):
    map(lambda f: str(f), numbers)
    output = ""
    curr_str = ""
    for x in range(25):
        curr_str += "1" if str(numbers[x]) in inp_str else "0"
        if len(curr_str) == 5:
            output += chr(int(curr_str, 2) + 64)
            curr_str = ""
    return output
