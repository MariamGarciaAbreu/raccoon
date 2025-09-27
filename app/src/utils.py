import datetime

def convert_month_num_to_name(month_num):
    return datetime.datetime(1, month_num, 1).strftime("%B")