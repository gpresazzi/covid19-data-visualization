import datetime


class DateHelper:

    @classmethod
    def date_to_str(cls, date: datetime.date):
        return date.strftime("%-m/%-d/%y")

    @classmethod
    def str_to_date(cls, date_str: str):
        return datetime.datetime.strptime(date_str, "%m/%d/%y")

    @classmethod
    def previous_day(cls, date: datetime.date):
        return date + datetime.timedelta(days=-1)

    @classmethod
    def previous_day_str(cls, date_str: str):
        date = datetime.datetime.strptime(date_str, "%m/%d/%y")
        return DateHelper.date_to_str(DateHelper.previous_day(date))

    @classmethod
    def decrement_day_str(cls, date_str: str, decrement=-1):
        date = datetime.datetime.strptime(date_str, "%m/%d/%y")
        date = date + datetime.timedelta(days=decrement)
        return DateHelper.date_to_str(date)

    @classmethod
    def increment_day_str(cls, date_str: str, increment=1):
        date = datetime.datetime.strptime(date_str, "%m/%d/%y")
        date = date + datetime.timedelta(days=increment)
        return DateHelper.date_to_str(date)
