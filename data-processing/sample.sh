#!/bin/bash
echo 'sample.sh checkpoint output; change PATH in script'

SAMPLE_PATH=~/char-rnn/
DATA2CSV_PATH=~/EDAN70/data-processing/data2csv.py
OUTPUT_PATH="${2:-sample.wav}"
data_file=sample."${3:-d1}"

echo $data_file

cd $SAMPLE_PATH
th sample.lua $1 -length 50000 > $data_file;

python $DATA2CSV_PATH $data_file sample.csv
csvmidi sample.csv sample.mid
mv sample.mid $OUTPUT_PATH

rm $data_file sample.csv

echo 'sample written to '$OUTPUT_PATH'.'
