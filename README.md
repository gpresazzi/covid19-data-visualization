Repo used to do some test with panda + altair.
The used dataset comes from [COVID-19 public data sets](https://github.com/CSSEGISandData/COVID-19.git)

This is a very simple project to generate some useful charts and represent how the COVID-19 is behaving

## Examples 

Example of histogram showing the number of people currently confirmed
![histogram](https://github.com/gpresazzi/covid19-data-visualization/blob/master/images/histogram_total.png)

Example of line chart for the confirmed infected people by day
![line chart](https://github.com/gpresazzi/covid19-data-visualization/blob/master/images/lines_chart.png)



## Installation

- 1 - Clone this repo
```bash
git clone https://github.com/gpresazzi/covid19-data-visualization.git
```
- 2 - Enter inside folder and create vene
```bash
cd covid19-data-visualization
python -m venv venv
source venv/bin/activate
pip install altair
```
- 3 - clone data set
```bash
git clone https://github.com/CSSEGISandData/COVID-19.git 
```

- 4 - run
```bash
1. python src/main.py confirmed
2. python src/main.py recovered
3. python src/main.py death
```

Extra args:
```bash
-f for the format to use (empty or 'html')
-o output file
```
