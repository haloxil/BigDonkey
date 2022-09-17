from curses.ascii import isspace
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
    if is_leap_year(year):
        max_years = 367
    max_years = 366

    for day in numbers[1:]:
        if day <= 0 or day >= max_years:
            continue
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
    temp = ""

    while count != 12:
        if date_list[index] != count:
            part1 += 7 * " " + ","
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

    new_year = 2001 + part1.index(' ')
    day_list = part1.split(",")
    output = [new_year]
    for i in range(len(day_list)):
        if day_list[i].isspace():
            continue

        if day_list[i] == "weekend":
            for j in range(7):
                date2 = datetime.datetime(new_year,i+1,j+1)
                if date2.weekday() == 5 or date2.weekday() == 6:
                    output.append((date2 - datetime.datetime(new_year,1,1)).days + 1)
            continue
        elif day_list[i] == "weekday":
            for j in range(7):
                date2 = datetime.datetime(new_year,i+1,j+1)
                if date2.weekday() == 0 or date2.weekday() == 1 or date2.weekday() == 2 or date2.weekday() == 3 or date2.weekday() == 4:
                    output.append((date2 - datetime.datetime(new_year,1,1)).days + 1)
            continue
        elif day_list[i] == "alldays":
            for j in range(7):
                output.append((datetime.datetime(new_year,i+1,j+1) - datetime.datetime(new_year,1,1)).days + 1)
            continue
        for k in range(len(day_list[i])):
            if day_list[i][k] == "m":
                for j in range(7):
                    date2 = datetime.datetime(new_year,i+1,j+1)
                    if date2.weekday() == 0:
                        output.append((date2 - datetime.datetime(new_year,1,1)).days + 1)

            if day_list[i][k] == "t" and k == 1:
                for j in range(7):
                    date2 = datetime.datetime(new_year,i+1,j+1)
                    if date2.weekday() == 1:
                        output.append((date2 - datetime.datetime(new_year,1,1)).days + 1)

            if day_list[i][k] == "w":
                for j in range(7):
                    date2 = datetime.datetime(new_year,i+1,j+1)
                    if date2.weekday() == 2:
                        output.append((date2 - datetime.datetime(new_year,1,1)).days + 1)

            if day_list[i][k] == "t" and k == 3:
                for j in range(7):
                    date2 = datetime.datetime(new_year,i+1,j+1)
                    if date2.weekday() == 3:
                        output.append((date2 - datetime.datetime(new_year,1,1)).days + 1)

            if day_list[i][k] == "f":
                for j in range(7):
                    date2 = datetime.datetime(new_year,i+1,j+1)
                    if date2.weekday() == 4:
                        output.append((date2 - datetime.datetime(new_year,1,1)).days + 1)

            if day_list[i][k] == "s" and k == 5:
                for j in range(7):
                    date2 = datetime.datetime(new_year,i+1,j+1)
                    if date2.weekday() == 5:
                        output.append((date2 - datetime.datetime(new_year,1,1)).days + 1)

            if day_list[i][k] == "s" and k == 6:
                for j in range(7):
                    date2 = datetime.datetime(new_year,i+1,j+1)
                    if date2.weekday() == 6:
                        output.append((date2 - datetime.datetime(new_year,1,1)).days + 1)

    output_dict = {"part1": part1, "part2": output}
    return json.dumps(output_dict)

def is_leap_year(year):
    if (year % 400 == 0) and (year % 100 == 0):
        return True
    elif (year % 4 ==0) and (year % 100 != 0):
        return True
    return False