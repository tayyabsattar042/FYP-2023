import json
def getValue(name,month_name,week,x):
    with open('Json/weekly.json') as f:
        data=json.load(f)
    data=data[name]
    value=0
    wValue=0
    week_values=[]
    if month_name in data:
        if week in data[month_name]:
            if x in data[month_name][week]:
                value=data[month_name][week][x]
        for weeks in data[month_name]:
            week_values.append(sum(data[month_name][weeks].values()))
            wValue=sum(data[month_name][weeks].values())
    return [str(value),wValue]

    
    
    
