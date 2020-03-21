#/bin/bash

dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
echo $dir

cd "$dir/COVID-19" && git pull
cd "$dir"
python3 src/main.py death -f html -o output/deaths.html
python3 src/main.py confirmed -f html -o output/confirmed.html
python3 src/main.py recovered -f html -o output/recovered.html