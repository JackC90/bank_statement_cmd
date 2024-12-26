from typing import Optional

def get_next_id(date: str, last_id: Optional[str]):
    if not last_id:
        return date + "-01"
    else:
        last_num = int(last_id.split("-")[-1])
        next_num = str((last_num + 1)).zfill(2)
        return date + "-" + next_num
    
def format_date(date_object):
    return date_object.strftime("%Y%m%d") if date_object else None

def are_dates_same_day(date_a, date_b):
    return date_a.year == date_b.year and date_a.month == date_b.month and date_a.day == date_b.day

def is_after_day(date_a, date_b):
    return date_a.year == date_b.year and date_a.month == date_b.month and date_a.day < date_b.day