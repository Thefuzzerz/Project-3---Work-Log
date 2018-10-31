import csv
import datetime
import re
from datetime import timedelta

def change():
    value = ['07/08/1997', 'Giggling', '5' , 'None']


    with open('work_log.csv', 'r', newline="") as csvfile:
        fieldnames = ['date','job_title','time_spent','notes']
        workreader = csv.DictReader(csvfile, fieldnames=fieldnames)
        lines = list(workreader)
        print(value)
        tom_index = ([index for (index, d) in enumerate(lines)
                     if d["date"] == value[0]
                     and d["job_title"] == value[1]])
        print(tom_index)

def test():
    with open('work_log.csv', 'r', newline="") as csvfile:
        fieldnames = ['date','job_title','time_spent','notes']
        workreader = csv.DictReader(csvfile, fieldnames=fieldnames)
        lines = list(workreader)

    lines[3]['date'] = '14/12/1983'
    print(lines)

    with open('work_log.csv', 'w') as csvfile:
        fieldnames = ['date','job_title','time_spent','notes']
        workwriter = csv.DictWriter(csvfile, fieldnames=fieldnames)
        workwriter.writerows(lines)


        #workwriter = csv.writer(csvfile)
        #workwriter.writerows(lines)

change()
