import os
import altair as alt
import pandas as pandas
from date_helper import DateHelper


class BaseCharts:
    col_name_countries = "Country/Region"

    def __init__(self, csv_file_path, num_countries=20):
        dir_path = os.getcwd()
        self.num_countries = num_countries
        csv_data = os.path.join(dir_path, csv_file_path)
        self._data = pandas.read_csv(csv_data)
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
            y=alt.Y(day_str, axis=alt.Axis(format='N', title='TOT cases {}'.format(day_str)))
        ).interactive()
        return chart

    def get_histogram_increment_last_day(self, day_str):
        chart_data = self._data
        col_name_increments = "increments"
        chart_data[col_name_increments] = self._data[day_str] - self._data[DateHelper.previous_day_str(day_str)]
        chart_data = self._data[[self.col_name_countries, col_name_increments]]
        chart_data = chart_data.groupby(self.col_name_countries, as_index=False).agg({col_name_increments: "sum"})
        chart_data = chart_data.sort_values(by=[col_name_increments], ascending=False)
        chart_data = chart_data[:self.num_countries]

        chart = alt.Chart(chart_data).mark_bar().encode(
            x=alt.X(self.col_name_countries, sort='-x'),
            y=alt.Y(col_name_increments, axis=alt.Axis(format='N', title='daily increments on {}'.format(day_str)))
        ).interactive()
        return chart

    def get_chart_increment_per_day(self, day_str, num_previous_days=30, title=""):
        col_name_date = "date"
        col_name_value = "increments per day"

        # Get the top affected countries
        top_countries_data = self._data.groupby(self.col_name_countries, as_index=False).agg({day_str: "sum"})
        top_countries = top_countries_data.sort_values(
            by=[day_str], ascending=False
        )[:self.num_countries][self.col_name_countries]

        # print(top_countries)
        # Filter only the top countries data
        chart_data = self._data[self._data["Country/Region"].isin(top_countries.values)]
        # print(chart_data)

        data_1 = pandas.DataFrame()
        current_date_str = day_str
        for x in range(num_previous_days):
            previous_day = DateHelper.previous_day_str(current_date_str)

            data_tmp = pandas.DataFrame()
            data_tmp[self.col_name_countries] = chart_data[self.col_name_countries]
            data_tmp[col_name_date] = pandas.to_datetime(current_date_str, format='%m/%d/%y', errors='ignore')
            data_tmp[col_name_value] = chart_data[current_date_str] - chart_data[previous_day]
            data_tmp = data_tmp.groupby([self.col_name_countries, col_name_date], as_index=False).agg(
                {col_name_value: "sum"})

            data_1 = pandas.concat([data_1, data_tmp], ignore_index=True)
            current_date_str = previous_day

        nearest = alt.selection(type='single', nearest=True, on='mouseover',
                                fields=['date'], empty='none')
        line = alt.Chart(data_1).mark_line().encode(
            y=alt.Y("{}:Q".format(col_name_value)),
            x=alt.X('{}:T'.format(col_name_date), axis=alt.Axis(title='Date'.upper(), format="%d/%m/%Y")),
            color=alt.Color('{}'.format(self.col_name_countries), scale=alt.Scale(scheme='category20c'), 
                            legend=alt.Legend(orient='right')),
            tooltip='{}'.format(self.col_name_countries),
        )

        selectors = alt.Chart(data_1).mark_point().encode(
            x=alt.X('{}:T'.format(col_name_date), axis=alt.Axis(title='Date'.upper(), format="%d/%m/%Y")),
            opacity=alt.value(0),
        ).add_selection(
            nearest
        )

        # Draw points on the line, and highlight based on selection
        points = line.mark_point().encode(
            opacity=alt.condition(nearest, alt.value(1), alt.value(0))
        )

        # Draw text labels near the points, and highlight based on selection
        text = line.mark_text(align='left', dx=5, dy=-5).encode(
            text=alt.condition(nearest, '{}'.format(self.col_name_countries), alt.value(' '))
        )

        # Draw a rule at the location of the selection
        rules = alt.Chart(data_1).mark_rule(color='gray').encode(
            x=alt.X('{}:T'.format(col_name_date)),
        ).transform_filter(
            nearest
        ).properties(
            title=title
        )

        chart = alt.layer(
            line, selectors, points, rules, text
        ).properties(
            width=800, height=500
        ).interactive()

        return chart
