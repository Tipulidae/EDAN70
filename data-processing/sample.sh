#!/bin/bash

# Samples a checkpoint created by Karpathy's char-rnn
# 	[output] : path to output file
#	[data_type] : data representation used to train the network
#	[temp] : temperature [0.0 - 1.0]
#	[seed] : random seed to sample with [0 - 125]

# Change path to theano-theano and data-processing files manually

echo 'sample.sh checkpoint [output] [data_type] [temp] [seed]
echo change PATH in script'

SAMPLE_PATH=~/EDAN70/char-rnn/
DATA2CSV_PATH=~/EDAN70/data-processing/data2csv.py
OUTPUT_PATH="${2:-sample.mp3}"
data_file=sample."${3:-d1}"
temperature="${4:-1}"
seed="${5:-123}"

echo $data_file

cd $SAMPLE_PATH
th sample.lua $1 -length 50000 -seed $seed -temperature $temperature > $data_file;

python $DATA2CSV_PATH $data_file sample.csv
csvmidi sample.csv sample.mid
timidity -Ow sample.mid
lame sample.wav sample.mp3
mv sample.mp3 $OUTPUT_PATH
mv sample.csv.ci $OUTPUT_PATH.ci
rm $data_file sample.csv sample.mid sample.wav

echo 'sample written to '$OUTPUT_PATH'.'
