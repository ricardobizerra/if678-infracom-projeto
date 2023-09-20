import datetime

def get_time():
    timestamp = datetime.datetime.now()
    time_formatted = timestamp.strftime("%H:%M:%S %d/%m/%Y")
    return time_formatted