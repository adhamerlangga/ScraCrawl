import datetime
from dateutil.relativedelta import relativedelta

def stringago2datetime(text):
    # convert string "3 days ago" to Python date
    # only string : years, months, days, hours, minutes, seconds, microseconds
    # cant handle string : year, month, day, hour, minute, second, microsecond
    value, unit, _ = text.split()
    past_time = datetime.datetime.now() - datetime.timedelta(**{unit: float(value)})
    return past_time

def stringago2datetime_custom(str_days_ago):
    now = datetime.datetime.today()
    splitted = str_days_ago.split()
    if len(splitted) == 1 and splitted[0].lower() == 'today':
        return now
    elif len(splitted) == 1 and splitted[0].lower() == 'yesterday':
        time = now - relativedelta(days=1)
        return time
    elif splitted[1].lower() in ['microsecond', 'microseconds', 'microsec', 'microsecs', 'ms']:
        time = datetime.datetime.now() - relativedelta(minutes=int(splitted[0]))
        return time
    elif splitted[1].lower() in ['second', 'seconds', 'sec', 'secs', 's']:
        time = datetime.datetime.now() - relativedelta(minutes=int(splitted[0]))
        return time
    elif splitted[1].lower() in ['minute', 'minutes', 'min', 'mins', 'm']:
        time = datetime.datetime.now() - relativedelta(minutes=int(splitted[0]))
        return time
    elif splitted[1].lower() in ['hour', 'hours', 'hr', 'hrs', 'h']:
        time = datetime.datetime.now() - relativedelta(hours=int(splitted[0]))
        return time
    elif splitted[1].lower() in ['day', 'days', 'd']:
        time = now - relativedelta(days=int(splitted[0]))
        return time
    elif splitted[1].lower() in ['week', 'weeks', 'wk', 'wks', 'w']:
        time = now - relativedelta(weeks=int(splitted[0]))
        return time
    elif splitted[1].lower() in ['month', 'months', 'mon', 'mons', 'mo']:
        time = now - relativedelta(months=int(splitted[0]))
        return time
    elif splitted[1].lower() in ['year', 'years', 'yr', 'yrs', 'y']:
        time = now - relativedelta(years=int(splitted[0]))
        return time
    else:
        return "wrong argument format"

def remove_quotes(text):
    # strip the unicode quotes
    text = text.strip(u'\u201c'u'\u201d')
    return text


def convert_date(text):
    # convert string March 14, 1879 to Python date
    return datetime.strptime(text, '%B %d, %Y')