#Through this file i can enter/update  values weeks days

import json
import calendar
from datetime import date
from datetime import datetime

import yearlyupdate
def date_for_weekly(bitingvalue,name):
    x=calendar.day_name[date.today().weekday()]
    now = datetime.now()



    # Determine the week number
    week = (now.day + 6 - now.weekday()) // 7
    if week==0:
        week=1
    # Print the week number
    week='week'+str(week)

    month_name=datetime.now().strftime('%B')
    x=x[0:3]
    print("It is running Date for weekly")


    with open('Json/weekly.json') as f:
        data=json.load(f)
    if name in data:
        if month_name in data[name]:
            if week in data[name][month_name]:
                if x in data[name][month_name][week]:
                    # data[month_name][week][x]=bitingvalue
                    data[name][month_name][week][x]+=bitingvalue
                else:
                    data[name][month_name][week][x] = bitingvalue
                # print(x in data[month_name][week])
            else:
                data[name][month_name][week]={}
                data[name][month_name][week][x] =bitingvalue
            # print(data['monthly'])
        else:
            data[name][month_name]={}
            data[name][month_name][week] = {}
            data[name][month_name][week][x] = bitingvalue
    else:
        data[name]={}
        data[name][month_name] = {}
        data[name][month_name][week] = {}
        data[name][month_name][week][x] = bitingvalue
    with open('Json/weekly.json','w') as f:
        json.dump(data,f)
    yearlyupdate.yearlyUpdate(name)