from datetime import datetime


def clean_date(date_raw_string):
    date_string = date_raw_string[date_raw_string.find(' '):].strip()
    return datetime.strptime(date_string, "%d %B %Y")


def clean_attendance(attendance_raw_string):
    return int(attendance_raw_string.split(' ')[3])


def clean_stadium(stadium_raw_string):
    stadium = stadium_raw_string.strip()
    str_end = stadium.strip()[1:].find('|')
    stadium = stadium[1:str_end].strip()
    return stadium


def clean_score(raw_score):
    return '{0}-{1}'.format(*raw_score)
