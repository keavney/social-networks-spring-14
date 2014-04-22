import sys

from nltk.tokenize import wordpunct_tokenize
import re
import nltk

from model import Record

class TweetRanker:
    def __init__(self, training_model, algorithm='GIS'):
        # Calculate feature set from provided word counts
        self.feature_set = {}
        for tweet in training_model:
            for k, v in tweet[0].items():
                self.feature_set[k] = v
        
        # Create classifier object
        self.classifier = nltk.classify.MaxentClassifier.train(training_model, algorithm, trace=0, max_iter=200)

    def calculate_tweet_score(self, text, followers):
        # Compare feature sets
        record = Record(1, text, followers)
        record.get_features_set(self.feature_set)
        probability = self.classifier.prob_classify(record.features_set)
        record.probability = probability.prob('1')

        # Calculate tweet score from provided tweet, user pair
        record.impact_score = record.probability * (float(record.followers)+1)
        return record.impact_score

def tweet_score_is_valid(score):
    return score >= 0

