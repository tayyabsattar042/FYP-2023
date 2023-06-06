# In this file i am monthly updating the values

import json
from datetime import datetime

def yearlyUpdate(name):
    month_name=datetime.now().strftime('%B')

    with open('Json/weekly.json') as f:
        data=json.load(f)
    data=data[name]
    week_values=[]
    for weeks in data[month_name]:
        week_values.append(sum(data[month_name][weeks].values()))
        print(weeks,' ',sum(data[month_name][weeks].values()))

    month_value=sum(week_values)
    with open('Json/yearly.json') as f:
        data=json.load(f)
    if name in data:
        data[name]['yearly'][month_name]=month_value
    else:
        data[name] = {}
        data[name]['yearly'] = {}
        data[name]['yearly'][month_name] = month_value
    with open('Json/yearly.json','w') as f:
        json.dump(data,f)