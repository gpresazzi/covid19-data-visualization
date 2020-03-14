import os
import altair as alt
import pandas as pandas
from date_helper import DateHelper


class CovidConfirmed:

    def __init__(self):
        csv_file = "COVID-19/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Confirmed.csv"
        dir_path = os.getcwd()
        csv_confirmed = os.path.join(dir_path, csv_file)
        self._data = pandas.read_csv(csv_confirmed)
        print(self._data.head())

    def has_coloumn(self, col_name):
        return col_name in self._data.columns

    def get_histogram_per_day(self, day_str, num_regions=20):
        chart_data = self._data[["Country/Region", day_str]]
        chart_data = chart_data.groupby('Country/Region', as_index=False).agg({day_str: "sum"})
        chart_data = chart_data.sort_values(by=[day_str], ascending=False)
        chart_data = chart_data[:num_regions]

        chart = alt.Chart(chart_data).mark_bar().encode(
            x=alt.X("Country/Region", sort='-x'),
            y=alt.Y(day_str)
        ).interactive()
        return chart

    def get_histogram_increment_last_day(self, day_str, num_regions=20):
        chart_data = self._data
        chart_data["increments"] = self._data[day_str] - self._data[DateHelper.previous_day_str(day_str)]
        chart_data = self._data[["Country/Region", "increments"]]
        chart_data = chart_data.sort_values(by=["increments"], ascending=False)
        chart_data = chart_data[:num_regions]

        chart = alt.Chart(chart_data).mark_bar().encode(
            x=alt.X("Country/Region", sort='-x'),
            y=alt.Y("increments", axis=alt.Axis(format='N', title='daily increments'))
        ).interactive()
        return chart

