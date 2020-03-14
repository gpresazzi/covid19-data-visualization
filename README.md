Repo used to do some test with panda + altair.
The used dataset comes from [COVID-19 public data sets](https://github.com/CSSEGISandData/COVID-19.git)


### Installation

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
python src/main.py
```