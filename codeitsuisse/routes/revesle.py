from random import Random, random, randrange
import re

import logging
import json

from flask import request, Response
from codeitsuisse import app

guesses = 0
rand_ele = lambda x: x[randrange(0,len(x))]
@app.route('/reversle', methods=['POST'])
def evaluate_reversle():
    data = request.get_json()
    eqn_len = data["equationLength"]
    attempts = data["attemptsAllowed"]
    output = guess(attempts,eqn_len,
                   data["equationHistory"] if "equationHistory" in data else None,
                   data["resultHistory"] if "resultHistory" in data else None)
    return Response(json.dumps({"equation":output}), mimetype='application/json')
    


def eval_stack_eqn(inp): #Evaluates a number from a stack.
    stack = []
    
    local_inp = inp[::-1]
    while(len(local_inp) > 0):
        nextChar = local_inp.pop()
        if re.match("[0-9]",nextChar): #Regex check for int
            stack.append(int(nextChar))
            continue
        else:
            if nextChar == "=":
                break; 
            
            num1 = stack.pop()
            num2 = stack.pop()
            if nextChar == "*":
                stack.append(num1 * num2)
            elif nextChar == "+":
                stack.append(num1 + num2)
            elif nextChar == "-":
                stack.append(num2 - num1)
            elif nextChar == "/":
                if num1 == 0: #Divided by 0
                    return None
                else:
                    stack.append(num2/num1)
            elif nextChar == "\\":
                if num2 == 0:
                    return None #Divided by 0
                else:
                    stack.append(num1/num2)
            elif nextChar == "^":
                if num2 == 0 and num1 < 0:
                    return None
                stack.append(num2**num1)
    return stack.pop()

def generate_possiblity_space(len):
    # Assumptions
    # '=' cannot exist in the first 3 index and the last index.
    # First 2 indexes can only be numbers
    # Can have as many of 1 type of number as mathematically possible
    # Format: LHS eqn must be odd length, with ceil(n/2) numbers and floor(n/2) ops
    # "=" therefore can only be in even positions.
    # Answer can be padded with as many 0s to fit problem, but not LHS.
    digits = "0123456789"
    ops = "\\/+-*^"

    output = []
    for x in range(len):
        current = []
        current += [digits]
        if x > 1:
            current += [ops]
            
        if (x > 2) and x % 2 == 1 and x != len - 1:
            current += ["="]
        output.append(current)
        
    return output
#Current dumb solution: Makes random guesses till 5 left to cut down solution space

def update_knowledge(space, guess, result):
    for index,ele in enumerate(result):
        if ele == "0": #Symbol Not Present
            for indexi,elei in enumerate(space):
                for indexj,elej in enumerate(elei):
                    space[indexi][indexj] = space[indexi][indexj].replace(guess[index],"")
            
        elif ele == "1":#Symbol present, but not here
            for indexi,elei in enumerate(space[index]):
                if guess[index] in elei:
                    space[index][indexi] = space[index][indexi].replace(guess[index],"")
        elif ele == "2": #THIS IS THE SYMBOL
            for indexi,elei in enumerate(space[index]):
                if guess[index] in elei:
                    space[index][indexi] = guess[index]
                else:
                    space[index][indexi] = ""
    return space


def guess(attempts,length, eqn_History, res_History):
    possiblity_space = generate_possiblity_space(length)
    if guesses >5:
        random_guesses = []
        #Exploration
        for x in range(50):
            random_guesses.append(make_guess(possiblity_space,length))
        return max(random_guesses,key = eval_fn)
    else:
        #Exploitation
        #cut down sln space
        space = generate_possiblity_space(length)
        for x in range(len(eqn_History)):
            space = update_knowledge(space, eqn_History[x], res_History[x])
    
        return make_guess(space,length)
            
    

def eval_fn(guess):
    return len(set(guess))

def make_guess(space, length):
    #Exploitation mode until guess = 5.
    used = set()
    attempts = 5
    
    def roll_unused_symbol(arr):
        this_symbol = rand_ele(arr)
        for x in range(attempts):
            if this_symbol in used:
                this_symbol = rand_ele(arr)
            else:
                break
        return this_symbol
    
    output = []
    eq_locs = []
    for index,ele in enumerate(space):
        if "=" in ele[-1]:
            eq_locs += [index]
    num_digits_ops = rand_ele(eq_locs)
    
    pending_digits = num_digits_ops // 2 + 1
    current_num_in_stack = 0
    

    for x in range(length):
        if x < num_digits_ops:
            if current_num_in_stack < 2 or \
                    (pending_digits > 0 and randrange(0,2) == 0):
                pending_digits -= 1
                current_num_in_stack += 1
                this_symbol = roll_unused_symbol(space[x][0])
                used.add(this_symbol)
                output += [this_symbol]
                continue
            else:
                current_num_in_stack -= 1
                this_symbol = roll_unused_symbol(space[x][1])
                used.add(this_symbol)
                output += [this_symbol]
                continue
        else:
            eqn_eval =  eval_stack_eqn(output)
            if eqn_eval == None or isinstance(eqn_eval, complex) or eqn_eval % 1 != 0 or eqn_eval < 0 or len(str(eqn_eval)) > length - num_digits_ops - 1: 
                #Divide by 0 or non int result or neg result or long result
                return make_guess(space,length) #Reroll
            else:
                ans_len = length - num_digits_ops
                rest_of_eqn = "=" + ('{:0>'+str(ans_len - 1)+'}').format(int(eqn_eval)) #Left pad ans with 0s
                output.extend(rest_of_eqn)
                return output
            
            
            
        
    
    


