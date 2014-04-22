import sys
import csv
import argparse
import ast

import trank.model
import trank.rank

# get arguments
parser = argparse.ArgumentParser(
    description="Run test data against a training model.")
parser.add_argument('-d', '--delimiter', default='|',
    help="CSV file delimiter. (Default: |)")
parser.add_argument('modelfile', nargs=1,
    help="Training model.")
parser.add_argument('testfile', nargs=1,
    help="CSV test model.")
args = parser.parse_args()

# load model and create tweet ranker
training_model = []
with open(args.modelfile[0], 'r') as f:
    m = f.read()
    training_model = ast.literal_eval(m)
ranker = trank.rank.TweetRanker(training_model)

# open csv file, rank each tweet, and add to list if it qualifies
records = trank.model.get_record_list_from_csv_filename(args.testfile[0], args.delimiter)
ranked_tweets = []
for record in records:
    text = record.message
    followers = record.followers
    score = ranker.calculate_tweet_score(text, followers)
    if trank.rank.tweet_score_is_valid(score):
        ranked_tweets.append((score, text))

# print out tweets and scores
for tweetpair in ranked_tweets:
    print tweetpair
