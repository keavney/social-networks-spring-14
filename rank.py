import sys
import csv
import argparse

import trank.model

# get arguments
parser = argparse.ArgumentParser(
    description="Create a word ranking model from twitter stream data.")
parser.add_argument('-d', '--delimiter', default='|',
    help="CSV file delimiter. (Default: |)")
parser.add_argument('-o', '--outfile',
    help="Model file for output. If left blank, data will be output to stdout.")
parser.add_argument('csvfile', nargs=1)
args = parser.parse_args()

# get training model from ranker
training_model = trank.model.create_model_from_csv_filename(args.csvfile[0], args.delimiter)

# output model
if args.outfile:
    with open(args.outfile, 'w') as outfile:
        outfile.write(str(training_model))
else:
    print training_model
