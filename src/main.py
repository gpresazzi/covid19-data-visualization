import datetime
import altair as alt
from covid_confirmed import CovidConfirmed
from date_helper import DateHelper

start_date = datetime.date(2020, 1, 22)
today = datetime.datetime.now()


def main():
    confirmed_case = CovidConfirmed()

    current_date = today
    date_str = DateHelper.date_to_str(current_date)
    while not confirmed_case.has_coloumn(date_str):
        date_str = DateHelper.previous_day_str(date_str)
    yday_str = DateHelper.previous_day_str(date_str)

    # Total of contagios in the last day
    chart1 = confirmed_case.get_histogram_per_day(date_str)

    # 
    chart2 = confirmed_case.get_histogram_per_day(yday_str)

    # Higher increments in the last day
    chart3 = confirmed_case.get_histogram_increment_last_day(date_str)

    # Show charts
    chart = alt.vconcat()
    chart |= chart1
    chart |= chart2
    chart |= chart3
    chart.serve()


main()
