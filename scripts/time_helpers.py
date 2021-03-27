import pytz
import datetime, os

### CONVERT FROM ONE TIME ZONE TO ANOTHER
def convert_timezone(_from,  to):

    # samples 'Africa/Lagos', 'US/Central'
    source_zone = pytz.timezone(_from)
    target_zone = pytz.timezone(to)
    curtime = source_zone.localize(datetime.datetime.now())
    curtime = curtime.astimezone(target_zone)

    return curtime


###  MAKE DATETIME AWARE OF SERVER TIMEZONE
def localize_time(time):

    target_zone = pytz.timezone(os.getenv("time_zone"))
    localized_time = target_zone.localize(time)

    return time


def convert_date(date):
    # RETURN DATE OBJECT FROM SET FORMAT DD-MM-YY HH:MM

    date_object = datetime.datetime.strptime(date, "%d-%m-%Y %H:%M")

    return date_object