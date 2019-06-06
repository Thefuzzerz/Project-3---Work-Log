"""
Work Log application for creating tasks by date and assigning
a job title, length of time and notes. Work log can be queried
through date parameters, job title and keyword.
"""



import csv
import datetime
from datetime import timedelta
import os
import platform
import re

def user_sys():
    """
    Detection of users operating system.
    """
    user = platform.system()
    return user

def clr_scr():
    """
    Function to clear screen based on operating system.
    """
    clr_method = user_sys()
    if clr_method == 'Linux':
        os.system('clear')
    else:
        os.system('cls')

def work_log():
    """
    Main function for work log.
    """
    clr_scr()
    while True:
        clr_scr()
        print("""\n\n
        ****** Treehouse Work Log Tracker ******\n
        What function would you like to perform?\n
        """)
        main_menu = ("Create New Entry", "Search Entries", "QUIT")
        search_options = ("Exact Date", "Range of Dates", "Exact Job Title",
                          "Keyword Search", "Time Spent", "Previous Menu",
                          "QUIT")
        choice = menu(main_menu)
        clr_scr()
        if choice == 1:
            clr_scr()
            print("***** Creating New Entry *****")
            create_entry()
        if choice == 2:
            clr_scr()
            print("***** Search Log Entries *****")
            search_type = menu(search_options)
            if search_type == 1:
                filter_date()
            if search_type == 2:
                values = range_search()
                if values is False:
                    pass
                else:
                    values = sort_dates(values)
                    list_control(values)

            elif search_type == 3:
                clr_scr()
                print('Search by Exact Job Title:\n')
                filter_job()

            elif search_type == 4:
                clr_scr()
                values = keyword_search()
                if values is not None:
                    list_control(values)
            elif search_type == 5:
                clr_scr()
                values = time_search()
                if values is not None:
                    list_control(values)

def menu(options):
    """
    Create many based on options.
    """
    while True:
        number = 1
        choices_num = len(options)
        for option in options:
            print(number, "-----", option)
            number += 1
        print("\nPlease make your selection")
        try:
            selection = int(input())
        except ValueError:
            clr_scr()
            print(f"\nPlease enter a value from 1 - {choices_num}\n")
            continue
        if selection == choices_num:
            clr_scr()
            quit()
        elif selection in range(1, choices_num):
            return selection
        else:
            print("Didn't work")

def keyword_search():
    """
    Search entries in csv for user keyword obtained from input.
    """
    clr_scr()
    with open('work_log.csv', 'r', newline="") as csvfile:
        fieldnames = ['date', 'job_title', 'time_spent', 'notes']
        workreader = csv.DictReader(csvfile, fieldnames=fieldnames)
        print('*** Search By Keyword ***\n')
        keyword = input('Enter Word or Phrase to Search:\n' +
                        'Enter X to Return\n')
        if keyword.lower() != 'x':
            count = 1
            found_keyword = []
            for row in workreader:
                if count == 1:
                    count += 1
                else:
                    if (re.search(keyword.lower(), row['job_title'].lower())
                            or re.search(keyword.lower(), row['notes'].lower())
                            != None):
                        found_keyword.append(list(row.values()))
            csvfile.close()
            return found_keyword

def sort_dates(value):
    """
    Convert string to date for sorting. Returns as string.
    """
    new_value = []
    count = 0
    for item in value:
        datetime_object = datetime.datetime.strptime(value[count][0], '%d/%m/%Y')
        item[0] = datetime_object
        new_value.append(item)
        count += 1
    new_value.sort()
    sorted_dates = []
    count = 0
    for item in new_value:
        datetime_object = item[0].strftime('%d/%m/%Y')
        item[0] = datetime_object
        sorted_dates.append(item)
        count += 1
    return sorted_dates

def create_csv():
    """
    Create work_log.csv if file does not exist.
    """
    try:
        with open('work_log.csv', 'x') as csvfile:
            fieldnames = ['date', 'job_title', 'time_spent', 'notes']
            workwriter = csv.DictWriter(csvfile, fieldnames=fieldnames)
            workwriter.writeheader()
        csvfile.close()
    except FileExistsError:
        pass
    try:
        os.remove('work_log_temp.csv')
    except IOError:
        pass

def create_entry():
    """
    Creation of entry based on user input.
    """
    new_entry = []
    # date
    while True:
        date = input('Enter X to Exit\nDate of the task\n' +
                     'Enter as DD/MM/YYYY: ')
        if date.lower() == 'x':
            return False
        if check_format(date) is True:
            if check_date(date) is True:
                new_entry.append(date)
                break
            else:
                print("Please enter a valid date.")
        else:
            print("Please use the requested format DD/MM/YYYY. ")
    #title
    clr_scr()
    while True:
        title = input("What is the name of the log?\n" +
                      "Enter X to Exit\n")
        if title.lower() == 'x':
            return False
        invalid_char = re.search(',', title)
        if invalid_char is not None:
            print('Invalid Special Character Used\n' +
                  'Hit Enter to Return\n')
            input()
            return False
        if title != '':
            new_entry.append(title)
            clr_scr()
            with open('work_log.csv', 'r') as csvfile:
                fieldnames = ['date', 'job_title', 'time_spent', 'notes']
                workreader = csv.DictReader(csvfile, fieldnames=fieldnames)
                for row in workreader:
                    if row['date'] == new_entry[0] and row['job_title'] == new_entry[1]:
                        print('Unable to Create -- Job Title exists' +
                              ' for that date.\nPlease try again.\n')
                        print('Hit Enter to Continue.')
                        input()
                        return False
                    else:
                        continue
            break
        else:
            print("Name Required For Log")
    #time_spent
    while True:
        try:
            time_spent = input("How long in minutes is the task?\n" +
                               "Enter X to Exit\n")
            if time_spent.lower() == 'x':
                return False
            time_spent = int(time_spent)
            if time_spent < 0:
                print("Number must be a postive integer")
            else:
                new_entry.append(time_spent)
                break
        except ValueError:
            print("Please enter a valid number in minutes. ")
    #notes
    clr_scr()
    notes = input("Please add notes to this log if needed.\n" +
                  "Enter X to Exit\n")
    invalid_char = re.search(',', notes)
    if notes.lower() == 'x':
        return False
    if invalid_char is not None:
        print('Invalid Special Character Used\n' +
              'Hit Enter to Return\n')
        input()
        return False
    new_entry.append(notes)
    with open('work_log.csv', 'a') as csvfile:
        fieldnames = ['date', 'job_title', 'time_spent', 'notes']
        workwriter = csv.DictWriter(csvfile, fieldnames=fieldnames)
        workwriter.writerow({
            'date': new_entry[0],
            'job_title': new_entry[1],
            'time_spent': new_entry[2],
            'notes': new_entry[3]
            })
    clr_scr()
    csvfile.close()
    print(f"The Work Log -- {new_entry[1]} -- has been created")
    input("Press Enter to Continue")

def date_range(start_date, end_date):
    """
    Create date range based on user input.
    """
    for date in range(int((end_date - start_date).days)+1):
        yield start_date + timedelta(date)

def change_value(value):
    """
    Change value of selection made in list of entries found.
    """
    while True:
        new_line = {'date':value[0], 'job_title' : value[1],
                    'time_spent' : value[2], 'notes' : value[3]}
        old_line = {'date':value[0], 'job_title' : value[1],
                    'time_spent' : value[2], 'notes' : value[3]}
        print("*** Change Value of Log: ***\n"
              f"(1) -- Date: {value[0]}\n"
              f"(2) -- Job Title: {value[1]}\n"
              f"(3) -- Time Spent: {value[2]}\n"
              f"(4) -- Notes: {value[3]}\n"
              f"(5) -- Exit")
        try:
            choice = int(input('Select value to change\n'))
        except ValueError:
            clr_scr()
            print('Invalid Option Selected\n')
            print('Hit Enter to Return\n')
            input()
            return False
        if choice in range(1, 5):
            if choice == 1:
                clr_scr()
                print(f'Enter a new value for {value[choice-1]}\n' +
                      'Enter X to Exit Without Changes\n')
                new_date = input("Date of the task\nEnter as DD/MM/YYYY: ")
                if new_date.lower() == 'x':
                    return False
                elif check_format(new_date) is True:
                    if check_date(new_date) is True:
                        new_line['date'] = new_date
                    else:
                        print("Please enter a valid date.")
                else:
                    print("Please use the requested format DD/MM/YYYY. ")

            if choice == 2:
                clr_scr()
                print(f'Enter a new Job Title for -- {value[choice-1]}\n' +
                      'Enter X to Exit to Exit Without Changes\n')
                new_title = input("New Job Title\n")
                if re.search(',', new_title) is True:
                    print('Invalid Special Character Used\n' +
                          'Hit Enter to Return\n')
                    return False
                if new_title.lower() == 'x':
                    return False
                else:
                    with open('work_log.csv', 'r') as csvfile:
                        fieldnames = ['date', 'job_title', 'time_spent',
                                      'notes']
                        workreader = csv.DictReader(csvfile,
                                                    fieldnames=fieldnames)
                        for row in workreader:
                            if (row['date'] == value[0]
                                    and row['job_title'].lower()
                                    == new_title.lower()):
                                print('Unable to Create -- Job Title exists' +
                                      ' for that date.\nPlease try again.\n')
                                print('Hit Enter to Continue.')
                                input()
                                csvfile.close()
                                return False
                            else:
                                new_line['job_title'] = new_title
                                continue
            if choice == 3:
                clr_scr()
                print(f'Enter Time Spent for {value[1]}\n' +
                      'Enter X to Exit Without Changes\n')
                while True:
                    new_time_spent = input("New Duration of Log: ")
                    if new_time_spent.lower() == 'x':
                        return False
                    try:
                        new_time_spent = int(new_time_spent)
                        if new_time_spent <= 0:
                            print("Number must be a postive integer")
                        else:
                            new_line['time_spent'] = new_time_spent
                            break
                    except ValueError:
                        print("Invalid Entry -- Enter a Valid Number")
            if choice == 4:
                clr_scr()
                print(f'Enter New Notes for {value[1]}\n' +
                      'Enter X to Exit Without Changes\n')
                new_notes = input("New Notes for Log: ")
                if re.search(',', new_notes) is True:
                    print('Invalid Special Character Used\n' +
                          'Hit Enter to Return\n')
                    return False
                if new_notes.lower() == 'x':
                    return False
                else:
                    new_line['notes'] = new_notes
            elif choice == 5:
                return False
        if choice == 5:
            break
        else:
            with open('work_log_temp.csv', 'x') as temp_file:
                fieldnames = ['date', 'job_title', 'time_spent', 'notes']
                with open('work_log.csv', 'r') as csvfile:
                    workreader = csv.DictReader(csvfile,
                                                fieldnames=fieldnames)
                    workwriter = csv.DictWriter(temp_file,
                                                fieldnames=fieldnames)
                    for row in workreader:
                        if (row['date'] == old_line['date']
                                and row['job_title'] == old_line['job_title']
                                and row['time_spent'] == old_line['time_spent']
                                and row['notes'] == old_line['notes']):
                            pass
                        else:
                            workwriter.writerow(row)
                    workwriter.writerow({
                        'date': new_line['date'],
                        'job_title': new_line['job_title'],
                        'time_spent': new_line['time_spent'],
                        'notes': new_line['notes']
                        })
                    clr_scr()
                    print('Change Successful - Hit Enter to Continue')
                    input()
                csvfile.close()
            temp_file.close()
            os.remove('work_log.csv')
            os.rename('work_log_temp.csv', 'work_log.csv')
            return False

def check_format(date):
    """
    Verification of date format entered.
    """
    check_input = r"\d\d/\d\d/\d{4}"
    correct = bool(re.match(check_input, date))
    return correct

def check_date(date):
    """
    Value verification of date.
    """
    try:
        datetime.datetime.strptime(date, '%d/%m/%Y')
        return True
    except ValueError:
        return False

def filter_date():
    """
    Function to obtain date from user.
    """
    clr_scr()
    with open('work_log.csv', 'r', newline="") as csvfile:
        fieldnames = ['date', 'job_title', 'time_spent', 'notes']
        workreader = csv.DictReader(csvfile, fieldnames=fieldnames)
        while True:
            print('Enter X to Exit\n')
            date = input("Enter Filter Date DD/MM/YYYY: ")
            if date.lower() == 'x':
                return False
            if check_format(date) is True:
                if check_date(date) is True:
                    values = []
                    for row in workreader:
                        if row['date'] == date:
                            values.append(list(row.values()))
                    if values is False:
                        print("No Jobs were found for the selected date")
                        input("Press Enter to Return")
                        break
                    else:
                        csvfile.close()
                        list_control(values)
                        break
                else:
                    print("Please enter a valid date.")

            else:
                print("Please use the proper format DD/MM/YYYY: ")

def filter_job():
    """
    Filter job title in csv by user input.
    """
    with open('work_log.csv', 'r', newline="") as csvfile:
        fieldnames = ['date', 'job_title', 'time_spent', 'notes']
        workreader = csv.DictReader(csvfile, fieldnames=fieldnames)
        while True:
            job = input("\nEnter the Job Title - Enter X to Exit:\n")
            if job.lower() == 'x':
                return False
            values = []
            for row in workreader:
                if row['job_title'].lower() == job.lower():
                    values.append(list(row.values()))
            if values is False:
                print("No Jobs were found for the selected date")
                input("Press Enter to Return")
                return False
            list_control(values)
            return False

def range_value():
    """
    Date range function
    """
    while True:
        print('Enter X to Exit\n')
        range_entered = input("Please Enter Date DD/MM/YYYY:\n")
        if range_entered.lower() == 'x':
            return range_entered
        else:
            if check_format(range_entered) is True:
                if check_date(range_entered) is True:
                    range_entered = datetime.datetime.strptime(range_entered,
                                                               '%d/%m/%Y')
                    return range_entered
                else:
                    print("Please enter a valid date.")
            else:
                print("Please use the requested format DD/MM/YYYY. ")

def range_search():
    """
    Function to query csv file for logs within the date range.
    """
    while True:
        clr_scr()
        print('Search by Range - Start Date:\n')
        start_range = range_value()
        if start_range == '':
            return False
        clr_scr()
        print('Search by Range - End Date:\n')
        end_range = range_value()
        if end_range == '':
            return False
        if start_range > end_range:
            print('Start Date is Later than End Date\n' +
                  'Hit Enter to Return\n')
            input()
            return False
        clr_scr()
        values = []
        with open('work_log.csv', 'r', newline="") as csvfile:
            fieldnames = ['date', 'job_title', 'time_spent', 'notes']
            workreader = csv.DictReader(csvfile, fieldnames=fieldnames)
            for row in workreader:
                if row['date'] == 'date':
                    pass
                elif (datetime.datetime.strptime(row['date'], '%d/%m/%Y')
                      in date_range(start_range, end_range)):
                    values.append(list(row.values()))
            csvfile.close()
        return values

def time_search():
    """
    Function to query csv by time Spent
    """
    clr_scr()
    with open('work_log.csv', 'r', newline="") as csvfile:
        fieldnames = ['date', 'job_title', 'time_spent', 'notes']
        workreader = csv.DictReader(csvfile, fieldnames=fieldnames)
        print('*** Search By Time Spent ***\n')
        time_query = input('Enter Time Spent to Search Log:\n' +
                           'Enter X to Return\n')
        if time_query.lower() == 'x':
            return None
        elif time_query.lower() != 'x':
            count = 1
            found_time = []
            for row in workreader:
                if count == 1:
                    count += 1
                else:
                    if re.search(str(time_query), row['time_spent']) != None:
                        found_time.append(list(row.values()))

            csvfile.close()
            return found_time


def list_control(values):
    """
    List for returned values.
    """
    values = sort_dates(values)
    clr_scr()
    count = 0
    max_len = len(values)
    if max_len == 1:
        print("Work Log Found\n"
              f"Date: {values[count][0]}\n"
              f"Job Title: {values[count][1]}\n"
              f"Length of Time: {values[count][2]}\n"
              f"Notes: {values[count][3]}\n"
              "Hit Enter to Exit" +
              " [C] to Change Value -- [D] to Delete Entry\n")
        control = input()
        if control.lower() == 'c':
            while True:
                clr_scr()
                change_value(values[count])
                break
        elif control.lower() == 'd':
            delete_entry(values[count])
    elif max_len == 0:
        print('No Values Found\n')
        input("Hit Enter to Continue\n")
    else:
        while True:
            clr_scr()
            print("Multiple Work Logs Found\n"
                  f"Date: {values[count][0]}\n"
                  f"Job Title: {values[count][1]}\n"
                  f"Length of Time: {values[count][2]}\n"
                  f"Notes: {values[count][3]}\n")
            if count == 0:
                print('[N]ext -- [E]xit\n'
                      '[C] to Change Value -- [D] to Delete Entry\n')
                control = input()
                if control.lower() == 'c':
                    while True:
                        clr_scr()
                        change_value(values[count])
                        return False
                elif control.lower() == 'n':
                    count += 1
                elif control.lower() == 'e':
                    break
                elif control.lower() == 'd':
                    delete_entry(values[count])
                    break
                else:
                    print('Please enter a valid selection [N]][E]\n'
                          '[C] to Change Value -- [D] to Delete Entry\n')
            elif count in range(0, max_len-1):
                print('[P]revious -- [N]ext -- [E]xit\n'
                      '[C] to Change Value -- [D] to Delete Entry\n')
                control = input()
                if control.lower() == 'n':
                    count += 1
                elif control.lower() == 'c':
                    while True:
                        clr_scr()
                        change_value(values[count])
                        return False
                elif control.lower() == 'p':
                    count -= 1
                elif control.lower() == 'e':
                    break
                elif control.lower() == 'd':
                    delete_entry(values[count])
                    break
                else:
                    pass
            else:
                print('[P]revious -- [E]xit\n'
                      '[C] to Change Value -- [D] to Delete Entry\n')
                control = input()
                if control.lower() == 'p':
                    count -= 1
                elif control.lower() == 'c':
                    while True:
                        clr_scr()
                        change_value(values[count])
                        return False
                elif control.lower() == 'e':
                    break
                elif control.lower() == 'd':
                    delete_entry(values[count])
                    break
                else:
                    pass
    clr_scr()

def delete_entry(values):
    """
    Entry deletion function
    """
    clr_scr()
    while True:
        print(f'Confirm Deletion of {values[1]}\n')
        confirm = input('Enter (Y) to confirm -- (N) to cancel\n')
        if confirm.lower() == 'y':
            clr_scr()
            del_line = {'date': values[0], 'job_title': values[1],
                        'time_spent': values[2], 'notes': values[3]}
            with open('work_log_temp.csv', 'x') as temp_file:
                fieldnames = ['date', 'job_title', 'time_spent', 'notes']
                with open('work_log.csv', 'r') as csvfile:
                    workreader = csv.DictReader(csvfile,
                                                fieldnames=fieldnames)
                    workwriter = csv.DictWriter(temp_file,
                                                fieldnames=fieldnames)
                    for row in workreader:
                        if row['date'] == del_line['date']:
                            if row['job_title'] == del_line['job_title']:
                                pass
                        else:
                            workwriter.writerow(row)
                    print('Deletion of Log Successful - Hit Enter to Continue')
                    input()
                csvfile.close()
            temp_file.close()
            os.remove('work_log.csv')
            os.rename('work_log_temp.csv', 'work_log.csv')
            return False
        if confirm.lower() == 'n':
            break
        else:
            print('Please Enter Y or N\n')


if __name__ == "__main__":
    create_csv()
    work_log()
