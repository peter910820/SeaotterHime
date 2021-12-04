import datetime

def dateOperation():
    loc_dt = datetime.datetime.today() 
    time_del = datetime.timedelta(hours=8) 
    new_dt = loc_dt + time_del 
    time_format = new_dt.strftime("%H:%M:%S")
    date_format = new_dt.strftime("%Y/%m/%d")
    timeDate = [time_format, date_format]
    return timeDate