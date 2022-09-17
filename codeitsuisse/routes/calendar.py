import logging
import json

import datetime

from flask import request, Response

from codeitsuisse import app

logger = logging.getLogger(__name__)


@app.route('/calendarDays', methods=['POST'])
def evaluate_calendar():
    data = request.get_json()
    count = 1
    part1 = ""
    date_dic = {}

    numbers = data["numbers"]
    year = numbers[0]

    for day in numbers[1:]:
        date = datetime.datetime(year,1,1) + datetime.timedelta(day - 1)
        datem = date.strptime(str(date), "%Y-%m-%d %H:%M:%S")
        day_of_week = date.weekday()
        if datem.month not in date_dic:
            date_dic[datem.month] = str(day_of_week)
        else:
            if str(day_of_week) not in date_dic[datem.month]:
                date_dic[datem.month] += str(day_of_week)

    date_list = list(date_dic.keys())
    date_list.sort()
    for key in date_list:
        while count != 13:
            if key != count:
                part1 += 7 * " " + ","
            elif "0" in date_dic[key] and "1" in date_dic[key] and "2" in date_dic[key] and "3" in date_dic[key] and "4" in date_dic[key] and "5" in date_dic[key] and "6" in date_dic[key]:
                part1 += "alldays,"
            elif "0" in date_dic[key] and "1" in date_dic[key] and "2" in date_dic[key] and "3" in date_dic[key] and "4" in date_dic[key]:
                part1 += "weekday,"
            elif "5" in date_dic[key] and "6" in date_dic[key]:
                part1 += "weekend,"
            else:
                if "0" in date_dic[key]:
                    part1 += "m"
                else:
                    part1 += " "
                if "1" in date_dic[key]:
                    part1 += "t"
                else:
                    part1 += " "
                if "2" in date_dic[key]:
                    part1 += "w"
                else:
                    part1 += " "
                if "3" in date_dic[key]:
                    part1 += "t"
                else:
                    part1 += " "
                if "4" in date_dic[key]:
                    part1 += "f"
                else:
                    part1 += " "
                if "5" in date_dic[key]:
                    part1 += "s"
                else:
                    part1 += " "
                if "6" in date_dic[key]:
                    part1 += "s"
                else:
                    part1 += " "
                part1 += ","

            count += 1

    output_dict = {"part1": [part1]}
    return json.dumps(output_dict)