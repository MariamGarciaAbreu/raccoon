import datetime

CURRENCY = "RD$"

def convert_month_num_to_name(month_num):
    return datetime.datetime(1, month_num, 1).strftime("%B")

def format_currency(amount):
    return f"{CURRENCY} {amount:,.2f}"