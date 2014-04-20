import sys
import tweepy
import math
from distance import distance_between

class Streamer:
    def __init__(self, credentials):
        self.auth = tweepy.OAuthHandler(
            credentials['consumer_key'], credentials['consumer_secret'])
        self.auth.set_access_token(
            credentials['access_token_key'], credentials['access_token_secret'])
        self.api = tweepy.API(self.auth)

    def read(self, action, keywords, quantity, center, distance):
        languages = ['en']
        listener = FilteredListener(self.api, action, quantity, center, distance)
        stream = tweepy.Stream(self.auth, listener)
        stream.filter(track = keywords, languages = languages)

class FilteredListener(tweepy.StreamListener):
    def __init__(self, api, action, quantity, center, distance):
        super(FilteredListener, self).__init__()
        self.count = 0
        self.api = api
        self.action = action
        self.quantity = quantity
        self.center = center
        self.distance = distance

    def on_status(self, tweet):
        if tweet.coordinates:
            d = math.ceil(distance_between(
                tweet.coordinates["coordinates"][1],
                tweet.coordinates["coordinates"][0],
                self.center["lat"],
                self.center["long"]))
            if d < self.distance:
                user = self.api.get_user(tweet.user.screen_name)
                self.action(tweet, user)
                self.count += 1
                if self.quantity > 0 and self.count >= self.quantity:
                    return False

