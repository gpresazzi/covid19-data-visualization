#/bin/bash

dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
echo $dir

cd "$dir/COVID-19" && git pull
cd "$dir"

# Generate HTML versions
# python3 src/main.py death -f html -o output/deaths.html
# python3 src/main.py confirmed -f html -o output/confirmed.html
# python3 src/main.py recovered -f html -o output/recovered.html

# Generate JSON versions
python3 src/main.py death -f json -o output/deaths.json
python3 src/main.py confirmed -f json -o output/confirmed.json
python3 src/main.py recovered -f json -o output/recovered.json

# Using template to generate HTML
sed 's/chart.json/deaths.json/g' html/template.html > output/deaths.html
sed 's/chart.json/confirmed.json/g' html/template.html > output/confirmed.html
sed 's/chart.json/recovered.json/g' html/template.html > output/recovered.html