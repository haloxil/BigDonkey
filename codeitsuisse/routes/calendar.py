import logging
import json

import datetime

from flask import request, Response

from codeitsuisse import app

logger = logging.getLogger(__name__)


@app.route('/calendarDays', methods=['POST'])
def evaluate_calendar():
    data = request.get_json()
    count = 0
    index = 0
    part1 = ""
    date_dic = {}

    numbers = data["numbers"]
    year = numbers[0]

    for day in numbers[1:]:
        date = datetime.datetime(year,1,1) + datetime.timedelta(day - 1)
        datem = date.strptime(str(date), "%Y-%m-%d %H:%M:%S")
        month = datem.month - 1
        day_of_week = date.weekday()
        if month not in date_dic:
            date_dic[month] = str(day_of_week)
        else:
            if str(day_of_week) not in date_dic[month]:
                date_dic[month] += str(day_of_week)

    if not bool (date_dic):
        for i in range(12):
            part1 += 7 * " " + ","

    date_list = list(date_dic.keys())
    date_list.sort()

    print(date_list)
    temp = ""

    while count != 12:
        if date_list[index] != count:
            part1 += 7 * " " + ","
        # elif "0" in date_dic[key] and "1" in date_dic[key] and "2" in date_dic[key] and "3" in date_dic[key] and "4" in date_dic[key] and "5" in date_dic[key] and "6" in date_dic[key]:
        #     part1 += "alldays,"
        # elif "0" in date_dic[key] and "1" in date_dic[key] and "2" in date_dic[key] and "3" in date_dic[key] and "4" in date_dic[key]:
        #     part1 += "weekday,"
        # elif "5" in date_dic[key] and "6" in date_dic[key]:
        #     part1 += "weekend,"
        else:
            if "0" in date_dic[date_list[index]]:
                temp += "m"
            else:
                temp += " "
            if "1" in date_dic[date_list[index]]:
                temp += "t"
            else:
                temp += " "
            if "2" in date_dic[date_list[index]]:
                temp += "w"
            else:
                temp += " "
            if "3" in date_dic[date_list[index]]:
                temp += "t"
            else:
                temp += " "
            if "4" in date_dic[date_list[index]]:
                temp += "f"
            else:
                temp += " "
            if "5" in date_dic[date_list[index]]:
                temp += "s"
            else:
                temp += " "
            if "6" in date_dic[date_list[index]]:
                temp += "s"
            else:
                temp += " "

            if temp == "mtwtfss":
                part1 += "alldays"
            elif temp == "mtwtf  ":
                part1 += "weekday"
            elif temp == "     ss":
                part1 += "weekend"
            else:
                part1 += temp
            
            temp = ""
            part1 += ","

            if index < len(date_list) - 1:
                index += 1

        count += 1

    output_dict = {"part1": part1, "part2": []}
    return json.dumps(output_dict)