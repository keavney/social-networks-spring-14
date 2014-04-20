import sys
import csv
import argparse

from tstream.stream import Streamer

# load account info
credentials = {}
with open("auth", "r") as fauth:
    for line in fauth:
        key, value = line.split()
        credentials[key] = value

# setup parameters
center = {'lat' : 40.7300, 'long' : -73.9950} # Washington Square Park
distance = 1000

# get arguments
parser = argparse.ArgumentParser(
    description="Collect twitter stream data for the provided keywords.")
parser.add_argument('-q', '--quantity', default='-1', type=int,
    help="Amount of tweets to collect. A value of -1 will collect tweets until the program is forcefully stopped.")
parser.add_argument('-d', '--delimiter', default='|',
    help="CSV file delimiter.")
parser.add_argument('-o', '--outfile',
    help="CSV file for output. If left blank, data will be output to stdout.")
parser.add_argument('terms', nargs='+')
args = parser.parse_args()

# call streamer
streamer = Streamer(credentials)
if args.outfile:
    out = open(args.outfile, 'wb')
    writer = csv.writer(out, delimiter=args.delimiter)
    streamer.read(lambda tweet: writer.writerow(["0", tweet.text.encode('utf-8')]),
        args.terms, args.quantity, center, distance)
    out.close()
else:
    streamer.read(lambda tweet: sys.stdout.write("0"+args.delimiter+tweet.text+'\n'),
        args.terms, args.quantity, center, distance)
