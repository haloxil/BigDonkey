
from random import Random, random, randrange
import re

import logging
import json
from flask import request, Response
from codeitsuisse import app

@app.route('/connect4', methods=['POST'])
def evaluate_four():
    data = request.get_json()
    battleId = data["battleId"]
    r = requests.get(url = "https://cis2022-arena.herokuapp.com/connect4/start/"+battleId, mimetype='event/stream')    
    
    return Response(json.dumps({"part1": step1ans, "part2": step2ans}), mimetype='event/stream')













FLIP_TABLE = "(╯°□°)╯︵ ┻━┻"

deep_copy_list = lambda x: [list(row) for row in x]





def generate_board():
    return [["","","","","","",""],
            ["","","","","","",""],
            ["","","","","","",""],
            ["","","","","","",""],
            ["","","","","","",""],
            ["","","","","","",""]]
    
def print_state(state):
    print("\n".join(map(lambda x : (" ".join(map( lambda z: "-" if z == "" else z, x))).lower(), state)))
    
def eval_fn(state):
    #print_state(state)
    a = diagonal_eval(state)
    b = cardinal_eval(state)
    #print(a["X"] + b["X"] - a["O"] - b["O"])
    return a["X"] + b["X"] - a["O"] - b["O"]

def diagonal_eval(state):
    score = {"X" : 0 , "O" : 0}
    
    path = [(0,0),(1,0),(2,0),(3,0),(4,0),(5,0),(6,0),(6,1),(6,2),(6,3),(6,4),(6,5)]
    for coord in path:
        current_x = coord[1]
        current_y = coord[0]
        prev = ''
        curr = 0
        while current_x < 6 and current_y >= 0:
            if state[current_x][current_y] == '':
                if curr > 1:
                    score[state[current_x - 1][current_y + 1]] += curr**3
                curr = 0
                prev = ''
                current_x += 1
                current_y -= 1
                continue
            
            if prev == state[current_x][current_y]:
                
                curr += 1
                #print("dupe dl", prev , current_x,current_y, curr)
            else:
                if curr > 1:
                    score[state[current_x - 1][current_y + 1]] += curr**3
                curr = 1
                prev = state[current_x][current_y]
                
            current_x += 1
            current_y -= 1
        
        if curr > 1 and state[current_x - 1][current_y + 1] != '':
            score [state[current_x - 1][current_y + 1]] += curr**3
            
    path = [(0,5),(0,4),(0,3),(0,2),(0,1),(0,0),(1,0),(2,0),(3,0),(4,0),(5,0),(6,0)]
    
    for coord in path:
        current_x = coord[1]
        current_y = coord[0]
        prev = ''
        curr = 0
        while current_x < 6 and current_y < 7:
            if state[current_x][current_y] == '':
                if curr > 1:
                    score[state[current_x - 1][current_y - 1]] += curr**6
                curr = 0
                prev = ''
                current_x += 1
                current_y += 1
                continue
            if prev == state[current_x][current_y]:
                
                curr += 1
                #print("dupe dR", prev , current_x,current_y, curr)
            else:
                if curr > 1:
                    score[state[current_x - 1][current_y - 1]] += curr**6
                curr = 1
                prev = state[current_x][current_y]
                
            current_x += 1
            current_y += 1
            
        if curr > 1 and state[current_x - 1][current_y - 1] != '':
            score [state[current_x - 1][current_y - 1]] += curr**6
    return score
    

def cardinal_eval(state):
    score = {"X" : 0 , "O" : 0}

    prev = ''
    curr = 0
    for x in range(len(state)):
        prev = ''
        curr = 0
        for y in range(len(state[0])):
            if state[x][y] == '':
                if curr > 1:
                    #print("!", curr, score[prev])
                    score[prev] += curr**6
                prev = ''
                curr = 0
                continue           
            if prev != state[x][y]:
                if curr > 1:
                    score[prev] += curr**6
                    curr = 0
                    
                prev = state[x][y]
                curr = 1
            else:
                curr += 1
        if curr > 1:
            score[prev] += curr**6
            curr = 0
    if curr > 1:
            score[prev] += curr**6
            curr = 0
    
    
    prev = ''
    curr = 0
    for y in range(len(state[0])):
        prev = ''
        curr = 0
        for x in range(len(state)):
            if state[x][y] == '':
                if curr > 1:
                    score[prev] += curr**6
                prev = ''
                curr = 0
                continue
            
            if prev != state[x][y]:
                if curr > 1:
                    score[prev] += curr**6
                    curr = 0
                    
                prev = state[x][y]
                curr = 1
            else:
                curr += 1
        if curr > 1:
            score[prev] += curr**6
            curr = 0
    if curr > 1:
        score[prev] += curr**6
        curr = 0
            
                
    return score


def generate_moves(state, player):
    return list(map(lambda x: make_move(state,x,player), ["A","B","C","D","E","F","G"]))

def make_move(state, clmn, player):
    current_state = deep_copy_list(state)
    changed = False
    index = ord(clmn) - 65
    for x in current_state[::-1]:
        if x[index] == "":
            x[index] = player
            changed = True
            break;
    if changed:
        return [current_state, clmn]
    else:
        return None

def max_player(current_state,depth,top_node):
    
    moves = filter(lambda item: item is not None,generate_moves(deep_copy_list(current_state),"X"))
    if depth == 1: #Base case
        print("Max" +"\t"+ str(depth))
        max_output =  max(deep_copy_list(moves), key = lambda x : eval_fn(x[0]))
        if top_node:
            return max_output[1]
        else:
            return max_output[0]
    else:
        max_output =  max(deep_copy_list(moves), key = lambda x : min_player(x[0], depth - 1, False))
        if top_node:
            return max_output[1]
        else:
            return max_output[0]
        
        
        

def min_player(current_state,depth,top_node):
    
    moves = filter(lambda item: item is not None,generate_moves(deep_copy_list(current_state),"O"))
    if depth == 1: #Base case
        #print("Max" +"\t"+ str(depth))
        min_output =  min(deep_copy_list(moves), key = lambda x : eval_fn(x[0]))
        if top_node:
            return min_output[1]
        else:
            return min_output[0]
    else:
        min_output =  min(deep_copy_list(moves), key = lambda x : max_player(x[0], depth - 1, False))
        if top_node:
            return min_output[1]
        else:
            return min_output[0]
        
        
    