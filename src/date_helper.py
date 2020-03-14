import datetime


class DateHelper:

    @classmethod
    def date_to_str(cls, date: datetime.date):
        return date.strftime("%-m/%-d/%y")

    @classmethod
    def previous_day(cls, date: datetime.date):
        return date + datetime.timedelta(days=-1)

    @classmethod
    def previous_day_str(cls, date_str: str):
        date = datetime.datetime.strptime(date_str, "%m/%d/%y")
        return DateHelper.date_to_str(DateHelper.previous_day(date))
