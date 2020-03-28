import os
import sys
import datetime
import altair as alt
from base_charts import BaseCharts
from map_charts import MapCharts
from date_helper import DateHelper
from cli_args import CLIArgs, OutputFormat

start_date = datetime.date(2020, 1, 22)
today = datetime.datetime.now()

csv_confirmed = "COVID-19/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv"
cvs_recovered = "COVID-19/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv"
cvs_death = "COVID-19/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv"

output_dir = "output/"


def main():
    args = CLIArgs.read_args(sys.argv[1:])
    if args.command == CLIArgs.CONFIRMED_COMMAND:
        charts = BaseCharts(csv_confirmed)
        map_builder = MapCharts(csv_confirmed)
    elif args.command == CLIArgs.RECOVERED_COMMAND:
        charts = BaseCharts(cvs_recovered)
        map_builder = MapCharts(cvs_recovered)
    elif args.command == CLIArgs.DEATHS_COMMAND:
        charts = BaseCharts(cvs_death)
        map_builder = MapCharts(cvs_death)

    if not args.output:
        filename = os.path.join(output_dir, "chart-{}.html".format(args.command))
    else:
        filename = args.output

    current_date = today
    date_str = DateHelper.date_to_str(current_date)
    while not charts.has_coloumn(date_str):
        date_str = DateHelper.previous_day_str(date_str)
    yday_str = DateHelper.previous_day_str(date_str)

    # Total of contagions in the last day
    chart_tot_per_day = charts.get_histogram_per_day(date_str)
    chart_increment_last = charts.get_histogram_increment_last_day(date_str)
    chart_lines_incr = charts.get_chart_increment_per_day(date_str,
                                                          title=f"Day by day increment of {args.command} patients")

    map_chart = map_builder.get_map(date_str, f"Worldwide map of {args.command} patients")

    chart_lines_tot = charts.get_chart_per_day(date_str, title="Total in top 20 countries")

    chart_row = alt.hconcat(chart_tot_per_day, chart_increment_last)
    chart = alt.vconcat(map_chart, chart_lines_tot, chart_lines_incr, chart_row)

    if args.format == OutputFormat.html:
        if not os.path.exists(output_dir):
            os.mkdir(output_dir)
        chart.save(filename)
        print("{} generated successfully !". format(filename))
    elif args.format == OutputFormat.json:
        if not os.path.exists(output_dir):
            os.mkdir(output_dir)
        chart.save(filename)
        print("{} generated successfully !". format(filename))
    else:
        chart.serve()


main()
