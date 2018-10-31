import datetime
from datetime import timedelta
import pytz
import os
import csv
import re


def work_log():

    create_csv()

    while True:
        clr_scr()
        print("""
        ****** Treehouse Work Log Tracker ******\n
        What function would you like to perform?\n
            (1) -- Create New Entry
            (2) -- Search Entries
            (3) -- QUIT
            """)
        choice = menu_select(top_value=3)

        if choice == 1:
            clr_scr()
            new_entry()

        if choice == 2:
            clr_scr()
            search_ent()

        if choice == 3:
            clr_scr()
            print("Thank you for using the TreeHouse Work Log")
            break

def search_ent():
    while True:
        clr_scr()
        print("""
        ****** Treehouse Work Log Tracker ******\n
        Select an option from below\n
        (1) -- Exact Date
        (2) -- Range of Dates
        (3) -- Exact Job Title
        (4) -- REGEX Query
        (5) -- Return to the Main Menu
            """)

        with open('work_log.csv', 'r', newline="") as csvfile:
            workreader = csv.DictReader(csvfile)
            choice = menu_select(top_value=5)
            clr_scr()

            if choice == 1:
                filter_date(workreader)

            elif choice == 2:
                print('Search by Range - Start Date:\n')
                start_range = range_value()
                clr_scr()
                print('Search by Range - End Date:\n')
                end_range = range_value()
                clr_scr()
                values = []
                for row in workreader:
                    if (datetime.datetime.strptime(row['date'], '%d/%m/%Y')
                    in date_range(start_range, end_range)):
                        values.append(list(row.values()))
                values.sort()
                list_control(values)

            elif choice == 3:
                filter_job(workreader)

            elif choice == 5:
                break

# Main menu prompt
def menu_select(top_value):
    while True:
        range_value= int(top_value)+1
        try:
            choice = int(input(f"Please enter your choice (1 - {top_value})"))
            if choice not in range(1,range_value) or type(choice) is not int:
                print(f"Please enter a value from 1 - {top_value}")
            if choice in range(1,range_value):
                return(choice)
                break
        except:
            print("Please enter a numerical value")

def range_value():
    while True:
        range_value = input("Please Enter Date DD/MM/YYYY:\n")
        if check_format(range_value) == True:
            if check_date(range_value) == True:
                range_value = datetime.datetime.strptime(range_value,
                                                         '%d/%m/%Y')
                return(range_value)
            else:
                print("Please enter a valid date.")
        else:
            print("Please use the requested format DD/MM/YYYY. ")
    pass

def filter_date(workreader):
    while True:
        date = input("Enter Filter Date DD/MM/YYYY: ")
        if check_format(date) == True:
            if check_date(date) == True:
                values = []
                for row in workreader:
                    if row['date'] == date:
                        values.append(list(row.values()))
                if len(values) == 0:
                    print("No Jobs were found for the selected date")
                    rtrn_menu = input("Press Enter to Return")
                    break
                else:
                    list_control(values)
                    break
            else:
                print("Please enter a valid date.")

        else:
            print("Please use the proper format DD/MM/YYYY: ")

def filter_job(workreader):
    while True:
        job = input("Enter the Job Title:\n")
        values = []
        for row in workreader:
            if row['job_title'].lower() == job.lower():
                values.append(list(row.values()))
        list_control(values)
        break
        if len(values) == 0:
            print("No Jobs were found for the selected date")
            rtrn_menu = input("Press Enter to Return")
            break

def date_range(start_date, end_date):
    for n in range(int ((end_date - start_date).days)+1):
        yield start_date + timedelta(n)

# Clear screen function
def clr_scr():
    os.system('cls' if os.name == 'nt' else 'clear')

def list_control(values):
    count = 0
    max_len = len(values)
    if max_len == 1:
        print(f"Date: {values[count][0]}\n"
              f"Job Title: {values[count][1]}\n"
              f"Length of Time: {values[count][2]}\n"
              f"Notes: {values[count][3]}\n")
        cont = input("Press Any Key to Continue -- [C] to Change Value\n")
    elif max_len == 0:
        print('No Values Found')
        cont = input("Press Any Key to Continue\n")
    else:
        while True:
            clr_scr()
            print(f"Date: {values[count][0]}\n"
                  f"Job Title: {values[count][1]}\n"
                  f"Length of Time: {values[count][2]}\n"
                  f"Notes: {values[count][3]}\n")
            if count == 0:
                control = input("[N]ext -- [E]xit -- [C] to Change Value\n")
                if control.lower() == 'c':
                    while True:
                        change_value(values[count])
                        break

                elif control.lower() == 'n':
                    count +=1
                elif control.lower() == 'e':
                    break
                else:
                    print('Please enter a valid selection [N]][E] -- [C] to Change Value\n')
            elif count in range(0,max_len-1):
                control = input("[P]revious --[N]ext -- [E]xit -- [C] to Change Value\n")
                if control.lower() == 'n':
                    count +=1
                elif control.lower() == 'p':
                    count -=1
                elif control.lower() == 'e':
                    break
                else:
                    print('Please enter a valid selection [P][N]][E] -- [C] to Change Value\n')
            else:
                control = input("[P]revious -- [E]xit\n")
                if control.lower() == 'p':
                    count -=1
                elif control.lower() == 'e':
                    break
                else:
                    print('Please enter a valid selection [P][E] -- [C] to Change Value\n')
    clr_scr()

def check_format(date):
    check_format = r"\d\d/\d\d/\d{4}"
    correct = bool(re.match(check_format, date))
    return correct

def check_date(date):
    try:
        check_date = datetime.datetime.strptime(date, '%d/%m/%Y')
        return True
    except:
        return False

def change_value(value):

    with open('work_log.csv', 'r', newline="") as csvfile:
        fieldnames = ['date','job_title','time_spent','notes']
        workreader = csv.DictReader(csvfile, fieldnames=fieldnames)
        lines = list(workreader)
        value_index = ([index for (index, d) in enumerate(lines)
                     if d["date"] == value[0]
                     and d["job_title"] == value[1]])
        clr_scr()

        print("*** Change Value of Log: ***\n"
             f"(1) -- Date: {value[0]}\n"
             f"(2) -- Job Title: {value[1]}\n"
             f"(3) -- Time Spent: {value[2]}\n"
             f"(4) -- Notes: {value[3]}\n"
             f"(5) -- Exit")
        choice = menu_select(top_value=5)
        while True:
            if choice == 1:
                change = write_change(value='date')
                confirmed = change_confirm(change)
                break
            elif choice == 2:
                change = write_change(value='job_title')
                break
            elif choice == 3:
                change = write_change(value='time_spent')
                break
            elif choice == 4:
                change = write_change(value='notes')
                break
            elif choice == 5:
                return False
        print(confirmed)
        input('Pause')

def write_change(value):
    value_change = ()
    clr_scr()
    if value == 'date':
        while True:
            new_value = input(f"New value for Date DD/MM/YYYY:\n")
            if check_format(new_value) == True:
                if check_date(new_value) == True:
                    value_change = ('date', new_value)
                    break
                else:
                    print("Please enter a valid date.")
            else:
                print("Please use the requested format DD/MM/YYYY. ")
    elif value == 'job_title':
        new_value = input(f"New value for Job Title:\n")
        value_change = ('job_title', new_value)
    elif value == 'time_spent':
        while True:
            try:
                new_value = int(input(f"New value for Time Spent:\n"))
                value_change = ('time_spent', new_value)
                break
            except:
                print('Please enter a valid number:\n')
    elif value == 'notes':
        new_value = input(f"New value for Notes:\n")
        value_change = ('notes', new_value)
    return(value_change)
    print(f"New {value_change[0]} is now {value_change[1]}\n")

# Creating csvfile with fieldnames - if exists will pass
def create_csv():
    try:
        with open('work_log.csv', 'x') as csvfile:
            fieldnames = ['date','job_title','time_spent','notes']
            workwriter = csv.DictWriter(csvfile, fieldnames=fieldnames)
            workwriter.writeheader()
    except:
        pass

def change_confirm(change):
    confirmed = None
    accept_change = input('Accept Changes? (Y)es/(n)o:\n')
    while True:
        if accept_change.lower() == 'y' or 'yes':
            confirmed = change
            return(confirmed)
            print(confirmed)
            input('YES')
        elif accept_change.lower() == 'n' or 'no':
            confirmed = ('decline')
            return(confirmed)
            print(confirmed)
            input('YES')
        else:
            print('Please Enter Y or N')
    return(confirmed)
    print(confirmed)
    input('returning')

def new_entry():

    new_entry = []

    # date
    while True:
        date = input("Date of the task\nEnter as DD/MM/YYYY: ")
        if check_format(date) == True:
            if check_date(date) == True:
                new_entry.append(date)
                break
            else:
                print("Please enter a valid date.")
        else:
            print("Please use the requested format DD/MM/YYYY. ")



    #title
    clr_scr()
    title = input("What is the name of the log? ")
    new_entry.append(title)

    #time_spent
    clr_scr()
    while True:
        try:
            time_spent = int(input("How long in minutes is the task? "))
            if time_spent < 0:
                 print("Number must be a postive integer")
            else:
                new_entry.append(time_spent)
                break
        except:
            print("Please enter a valid number in minutes. ")

    #notes
    clr_scr()
    notes = input("Please add notes to this log if needed. ")
    new_entry.append(notes)

    with open('work_log.csv', 'a') as csvfile:
        fieldnames = ['date','job_title','time_spent','notes']
        workwriter = csv.DictWriter(csvfile, fieldnames=fieldnames)
        workwriter.writerow({
            'date': new_entry[0],
            'job_title': new_entry[1],
            'time_spent': new_entry[2],
            'notes': new_entry[3]
    })

    clr_scr()
    print(f"The Work Log -- {new_entry[1]} -- has been created")
    rtrn_menu = input("Press Enter to Continue")

def edit_row(workreader,row):
    editreader = csv.reader(open(''))
    new_row = row


if __name__ == "__main__":
    work_log()
