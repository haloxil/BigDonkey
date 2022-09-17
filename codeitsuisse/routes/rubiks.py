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
    index = 0
    op_list = []

    while index < len(ops) - 1:
        if ops[index+1] == 'i':
            op = ops[index:index+2]
            index += 2
        else:
            op = ops[index]
            index += 1
        op_list.append(op)

    if ops[len(ops) - 1] != 'i':
        op_list.append(ops[len(ops) - 1])

    for elem in op_list:
        if elem == "U":
            u(state)
        if elem == "Ui":
            ui(state)
        if elem == "L":
            l(state)
        if elem == "Li":
            li(state)
        # if elem == "F":
        #     f(state)
        # if elem == "Fi":
        #     fi(state)
        if elem == "R":
            r(state)
        if elem == "Ri":
            ri(state)
        if elem == "D":
            d(state)
        if elem == "Di":
            di(state)

    return json.dumps(state)

def l(state):
    state['l'] = np.rot90(np.array(state['l']), 3).tolist()
    temp = np.array(state['u'])[:,0]
    temp2 = np.array(state['f'])[:,0]
    temp3 = np.array(state['d'])[:,0]

    for i in range(3):
        state['u'][0][i] = state['b'][0][i]
        state['f'][0][i] = int(temp[i])
        state['d'][0][i] = int(temp2[i])
        state['b'][0][i] = int(temp3[i])

def li(state):
    state['l'] = np.rot90(np.array(state['l']), 1).tolist()
    temp = np.array(state['u'])[:,0]
    temp2 = np.array(state['b'])[:,0]
    temp3 = np.array(state['d'])[:,0]

    for i in range(3):
        state['u'][0][i] = state['f'][0][i]
        state['b'][0][i] = int(temp[i])
        state['d'][0][i] = int(temp2[i])
        state['f'][0][i] = int(temp3[i])

def r(state):
    state['r'] = np.rot90(np.array(state['r']), 3).tolist()
    temp = np.array(state['b'])[:,2]
    temp2 = np.array(state['d'])[:,2]
    temp3 = np.array(state['f'])[:,2]

    for i in range(3):
        state['b'][2][i] = state['u'][2][i]
        state['d'][2][i] = int(temp[i])
        state['f'][2][i] = int(temp2[i])
        state['u'][2][i] = int(temp3[i])

def ri(state):
    state['r'] = np.rot90(np.array(state['r']), 1).tolist()
    temp = np.array(state['f'])[:,0]
    temp2 = np.array(state['d'])[:,0]
    temp3 = np.array(state['b'])[:,0]

    for i in range(3):
        state['f'][0][i] = state['u'][0][i]
        state['d'][0][i] = int(temp[i])
        state['b'][0][i] = int(temp2[i])
        state['u'][0][i] = int(temp3[i])

# def f(state):
#     state['l'] = np.rot90(np.array(state['l']), 3).tolist()
#     temp = np.array(state['u'])[:,0]
#     temp2 = np.array(state['f'])[:,0]
#     temp3 = np.array(state['d'])[:,0]

#     for i in range(3):
#         state['u'][0][i] = state['b'][0][i]
#         state['f'][0][i] = int(temp[i])
#         state['d'][0][i] = int(temp2[i])
#         state['b'][0][i] = int(temp3[i])

# def fi(state):
#     state['l'] = np.array(state['l']).transpose().tolist()
#     temp = np.array(state['u'])[:,0]
#     temp2 = np.array(state['b'])[:,0]
#     temp3 = np.array(state['d'])[:,0]

#     for i in range(3):
#         state['u'][0][i] = state['f'][0][i]
#         state['b'][0][i] = int(temp[i])
#         state['d'][0][i] = int(temp2[i])
#         state['f'][0][i] = int(temp3[i])

def u(state):
    state['u'] = np.rot90(np.array(state['u']), 3).tolist()
    temp = state['l'][0]
    state['l'][0] = state['f'][0]
    state['f'][0] = state['r'][0]
    state['r'][0] = state['b'][0]
    state['b'][0] = temp

def ui(state):
    state['u'] = np.rot90(np.array(state['u']), 1).tolist()
    temp = state['f'][0]
    temp2 = state['r'][0]
    temp3 = state['b'][0]
    state['f'][0] = state['l'][0]
    state['r'][0] = temp
    state['b'][0] = temp2
    state['l'][0] = temp3

def d(state):
    state['d'] = np.rot90(np.array(state['d']), 3).tolist()
    temp = state['f'][2]
    temp2 = state['r'][2]
    temp3 = state['b'][2]
    state['f'][2] = state['l'][2]
    state['r'][2] = temp
    state['b'][2] = temp2
    state['l'][2] = temp3

def di(state):
    state['d'] = np.rot90(np.array(state['d']), 1).tolist()
    temp = state['l'][2]
    state['l'][2] = state['f'][2]
    state['f'][2] = state['r'][2]
    state['r'][2] = state['b'][2]
    state['b'][2] = temp