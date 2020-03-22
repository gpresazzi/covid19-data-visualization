import os
import altair as alt
import pandas as pandas
from date_helper import DateHelper
from vega_datasets import data


class MapCharts:

    def __init__(self, csv_file):
        self._data = pandas.read_csv(csv_file)
        self.col_name_countries = "Country/Region"
        self.col_lat = "Lat"
        self.col_long = "Long"

    def _prepare_dataset(self, day_str):
        data_set = self._data[[self.col_name_countries, "Province/State", self.col_lat, self.col_long, day_str]]

        data_set = data_set.groupby([self.col_name_countries], as_index=False).agg(
            {
                self.col_long: "mean",
                self.col_lat: "mean",
                day_str: "sum"
            }
        )
        return data_set

    def get_map(self, day_str, title=""):
        chart_data = self._prepare_dataset(day_str)

        source = alt.topo_feature(data.world_110m.url, 'countries')
        background = alt.Chart(source).mark_geoshape(
            fill="lightgray",
            stroke="white"
        ).properties(
            width=1000, height=500
        ).project("equirectangular")

        hover = alt.selection(type='single', on='mouseover', nearest=False,
                              fields=[self.col_lat, self.col_long])
        text = background.mark_text(dy=-5, align='right').encode(
            alt.Text(f'{self.col_name_countries}:N', type='nominal'),
            opacity=alt.condition(~hover, alt.value(0), alt.value(1))
        )

        points = alt.Chart(chart_data).mark_circle().encode(
            latitude=f"{self.col_lat}:Q",
            longitude=f"{self.col_long}:Q",
            size=alt.Size(f"{day_str}:Q", scale=alt.Scale(range=[0, 7000]), legend=None),
            order=alt.Order(f"{day_str}:Q", sort="descending"),
            tooltip=[f'{self.col_name_countries}:N', f'{day_str}:Q']
        ).add_selection(
            hover
        ).properties(
            title=title
        )

        chart = alt.layer(background, points, text)

        return chart
