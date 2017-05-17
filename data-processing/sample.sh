#!/bin/bash
echo 'sample.sh checkpoint output; change PATH in script'

SAMPLE_PATH=~/char-rnn/
DATA2CSV_PATH=~/EDAN70/data-processing/data2csv.py
OUTPUT_PATH="${2:-sample.wav}"

cd $SAMPLE_PATH
th sample.lua $1 -length 5000 > sample.data;

python $DATA2CSV_PATH sample.data sample.csv
csvmidi sample.csv sample.mid
timidity -Ow sample.mid
mv sample.wav $OUTPUT_PATH

rm sample.data sample.mid sample.csv

echo 'sample written to '$OUTPUT_PATH'.'
