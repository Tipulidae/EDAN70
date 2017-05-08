#!/bin/bash

python ./data-processing/convert_csv.py
python ./data-processing/csv2data2.py
mv ./output.data ./char-rnn/data/input.txt
rm ./char-rnn/data/*.t7

cd ./char-rnn/
th train.lua -data_dir data/

