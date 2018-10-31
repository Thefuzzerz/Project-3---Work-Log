class Entry( date, title, time_spent, notes):
    def __init__(self, date, title, time_spent, notes):
        self.date = date
        self.title = title
        self.time_spent = time_spent
        self.notes = notes


    with open('work_log.csv', 'a') as csvfile:
        workwriter.writerow({
            'date': new_entry[0],
            'job_title': new_entry[1],
            'time_spent': new_entry[2],
            'notes': new_entry[3]
    })
