import os
import altair as alt
import pandas as pandas
from date_helper import DateHelper


class CovidConfirmed:
    col_name_countries = "Country/Region"

    def __init__(self, num_countries=20):
        csv_file = "COVID-19/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Confirmed.csv"
        dir_path = os.getcwd()
        self.num_countries = num_countries
        csv_confirmed = os.path.join(dir_path, csv_file)
        self._data = pandas.read_csv(csv_confirmed)
        print(self._data.head())

    def has_coloumn(self, col_name):
        return col_name in self._data.columns

    def get_histogram_per_day(self, day_str):
        chart_data = self._data[[self.col_name_countries, day_str]]
        chart_data = chart_data.groupby(self.col_name_countries, as_index=False).agg({day_str: "sum"})
        chart_data = chart_data.sort_values(by=[day_str], ascending=False)
        chart_data = chart_data[:self.num_countries]

        chart = alt.Chart(chart_data).mark_bar().encode(
            x=alt.X(self.col_name_countries, sort='-x'),
            y=alt.Y(day_str)
        ).interactive()
        return chart

    def get_histogram_increment_last_day(self, day_str):
        chart_data = self._data
        col_name_increments = "increments"
        chart_data[col_name_increments] = self._data[day_str] - self._data[DateHelper.previous_day_str(day_str)]
        chart_data = self._data[[self.col_name_countries, col_name_increments]]
        chart_data = chart_data.sort_values(by=[col_name_increments], ascending=False)
        chart_data = chart_data[:self.num_countries]

        chart = alt.Chart(chart_data).mark_bar().encode(
            x=alt.X(self.col_name_countries, sort='-x'),
            y=alt.Y(col_name_increments, axis=alt.Axis(format='N', title='daily increments'))
        ).interactive()
        return chart

    def get_chart_increment_per_day(self, day_str, num_previous_days=30):
        col_name_date = "date"
        col_name_value = "value"

        previous_day = DateHelper.previous_day_str(day_str)
        data_1 = pandas.DataFrame()
        data_1[self.col_name_countries] = self._data[self.col_name_countries]
        data_1[col_name_date] = pandas.to_datetime(day_str, format='%m/%d/%y', errors='ignore')
        data_1[col_name_value] = self._data[day_str] - self._data[previous_day]
        data_1 = data_1.groupby([self.col_name_countries, "date"], as_index=False).agg({col_name_value: "sum"})
        print(data_1.head())

        current_date_str = day_str
        for x in range(num_previous_days):
            previous_day = DateHelper.previous_day_str(current_date_str)

            data_tmp = pandas.DataFrame()
            data_tmp[self.col_name_countries] = self._data[self.col_name_countries]
            data_tmp[col_name_date] = pandas.to_datetime(previous_day, format='%m/%d/%y', errors='ignore')
            data_tmp[col_name_value] = self._data[day_str] - self._data[previous_day]
            data_tmp = data_tmp.groupby([self.col_name_countries, "date"], as_index=False).agg({col_name_value: "sum"})

            data_1 = pandas.concat([data_1, data_tmp], ignore_index=True)
            current_date_str = previous_day

        highlight = alt.selection(type='single', on='mouseover', fields=[self.col_name_countries], nearest=True)
        line = alt.Chart(data_1).mark_line().encode(
            y=alt.Y("value:Q"),
            x=alt.X('date:T', axis=alt.Axis(title='Date'.upper(), format="%d/%m/%Y")),
            color='{}:N'.format(self.col_name_countries)
        )

        selectors = alt.Chart(data_1).mark_point().encode(
            x=alt.X('date:T'),
            opacity=alt.value(0),
        ).add_selection(
            highlight
        )

        # Draw points on the line, and highlight based on selection
        points = line.mark_point().encode(
            opacity=alt.condition(highlight, alt.value(1), alt.value(0))
        )

        # Draw text labels near the points, and highlight based on selection
        text = line.mark_text(align='left', dx=5, dy=-5).encode(
            text=alt.condition(highlight, "value:Q", alt.value(' '))
        )

        # Draw a rule at the location of the selection
        rules = alt.Chart(data_1).mark_rule(color='gray').encode(
            x=alt.X('date:T'),
        ).transform_filter(
            highlight
        )

        chart = alt.layer(
            line, selectors, points, rules, text
        ).properties(
            width=600, height=300
        ).interactive()

        return chart
