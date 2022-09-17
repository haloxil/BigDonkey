import logging
import json
import queue
import heapq
import math
import pyjson5

from flask import request, Response

from codeitsuisse import app

logger = logging.getLogger(__name__)
@app.route('/hello', methods=['GET'])
def default_routeStig():
    return "Hello Template"

@app.route('/stig/warmup', methods=['POST'])
def stig_warmup():
    data = pyjson5.decode(request.get_data(as_text=True))
    output = []
    for i in range(len(data)):
        output.append(stig_warmup_logic(data[i]))
    return Response(json.dumps(output),mimetype='application/json')


def stig_warmup_logic(interview):
    max = interview["maxRating"]
    questions = interview["questions"]
    p=0
    q=0
    for real_value in range(1,max+1):
        possible_values = SLinkedList()
        for i in range(max,0,-1):
            possible_values.AtBegining(i)
        for i in range(len(questions)):
            if questions[i]["lower"] <= real_value <= questions[i]["upper"]:
                possible_values.KeepRange(questions[i]["lower"],questions[i]["upper"])
            else:
                possible_values.RemoveRange(questions[i]["lower"],questions[i]["upper"])
        if possible_values.head.data == real_value:
            p += 1
    gcd = math.gcd(p,max)
    return {"p": int(p / gcd), "q": int(max / gcd)}

@app.route('/stig/full', methods=['POST'])
def stig_full():
    data = pyjson5.decode(request.get_data(as_text=True))
    output = []
    for i in range(len(data)):
        output.append(stig_full_logic(data[i]))
    return Response(json.dumps(output), mimetype='application/json')

def stig_full_logic(interview):
    max = interview["maxRating"]
    questions = interview["questions"]
    lucky = interview["lucky"]
    p=1
    possibility_array = [0]
    for real_value in range(1,max+1):
        possible_values = SLinkedList()
        for x in range(max,0,-1):
            possible_values.AtBegining(x)
        possibility_array.append(possible_values)
    for question_id in range(len(questions)):
        for real_value in range(1,max+1):
            if questions[question_id]["lower"] <= real_value <= questions[question_id]["upper"]:
                possibility_array[question_id].KeepRange(questions[question_id]["lower"],questions[question_id]["upper"])
            else:
                possibility_array[question_id].RemoveRange(questions[question_id]["lower"],questions[question_id]["upper"])
            if possibility_array[question_id].head.data == real_value:
                p += 1
        gcd = math.gcd(p,max)
        p = int(p / gcd)
    return {"p": int(p / gcd), "q": int(max / gcd)}

class Node:
    def __init__(self, data=None):
        self.data = data
        self.next = None

class SLinkedList:
    def __init__(self):
        self.head = None

    def AtBegining(self, data_in):
        NewNode = Node(data_in)
        NewNode.next = self.head
        self.head = NewNode

    # Function to remove node
    def RemoveNode(self, Removekey):
        HeadVal = self.head

        if (HeadVal is not None):
            if (HeadVal.data == Removekey):
                self.head = HeadVal.next
                HeadVal = None
                return
        while (HeadVal is not None):
            if HeadVal.data == Removekey:
                break
            prev = HeadVal
            HeadVal = HeadVal.next

        if (HeadVal == None):
            return

        prev.next = HeadVal.next
        HeadVal = None

    def RemoveRange(self, itemLeft, itemRight):
        HeadVal = self.head
        foundLeft = False
        lastLeft = None
        prev = None
        while (HeadVal is not None):
            while not foundLeft:
                if(HeadVal == None): return
                if HeadVal.data >= itemLeft:
                    foundLeft = True
                    lastLeft = prev
                else:
                    prev = HeadVal
                    HeadVal = HeadVal.next
            if HeadVal.data > itemRight:
                break
            prev = HeadVal
            HeadVal = HeadVal.next

        if (HeadVal == None):
            lastLeft.next = None
            return
        if(lastLeft != None):
            lastLeft.next = HeadVal
        else:
            self.head = HeadVal
        HeadVal = None

    def KeepRange(self, itemLeft, itemRight):
        HeadVal = self.head
        foundLeft = False

        while (HeadVal is not None):
            while not foundLeft:
                if HeadVal.data >= itemLeft:
                    foundLeft = True
                    self.head = HeadVal
                else:
                    prev = HeadVal
                    HeadVal = HeadVal.next
            if HeadVal.data > itemRight:
                break
            prev = HeadVal
            HeadVal = HeadVal.next

        if (HeadVal == None):
            return

        prev.next = None
        HeadVal = None

    def LListprint(self):
        printval = self.head
        while (printval):
            print(printval.data),
            printval = printval.next