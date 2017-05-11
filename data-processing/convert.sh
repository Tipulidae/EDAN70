#!/bin/bash

cd ..
python ./data-processing/midi2csv.py
python ./data-processing/csv2data2.py
mv ./output.data ./char-rnn/data/input.txt
cd ./char-rnn/
rm ./data/*.t7

th train.lua -data_dir data/

