import sys
import argparse
import ast

import trank.model
import trank.rank

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
    description="Run twitter stream data against a training model.")
parser.add_argument('-q', '--quantity', default='-1', type=int,
    help="Amount of tweets to collect. A value of -1 will collect tweets until the program is forcefully stopped. (Default: -1)")
parser.add_argument('-o', '--outfile',
    help="File for output. If left blank, data will be output to stdout.")
parser.add_argument('modelfile', nargs=1,
    help="Training model.")
parser.add_argument('keywords', nargs='+')
args = parser.parse_args()

# load model and create tweet ranker
training_model = []
with open(args.modelfile[0], 'r') as f:
    m = f.read()
    training_model = ast.literal_eval(m)
ranker = trank.rank.TweetRanker(training_model)

# call streamer
streamer = Streamer(credentials)
if args.outfile:
    with open(args.outfile, 'wb') as outfile:
        action = (lambda tweet, user: outfile.write('('+str(ranker.calculate_tweet_score(tweet.text, user.followers_count)/user.followers_count)+', '+tweet.text.encode('utf-8')+')\n'))
        streamer.read(action, args.keywords, args.quantity, center, distance)
else:
    action = (lambda tweet, user: sys.stdout.write('('+str(ranker.calculate_tweet_score(tweet.text, user.followers_count)/user.followers_count)+', '+tweet.text+')\n'))
    streamer.read(action, args.keywords, args.quantity, center, distance)
