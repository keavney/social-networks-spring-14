import sys
from tstream.stream import Streamer
#from tstream.csv import CSVWriter

# load account info
credentials = {}
with open("auth", "r") as fauth:
    for line in fauth:
        key, value = line.split()
        credentials[key] = value

# output info
filename = "train.csv"

# setup parameters
terms = ['beer', 'party', 'fire']
quantity = 5
center = {'lat' : 40.7300, 'long' : -73.9950} # Washington Square Park
distance = 1000

# call streamer
try:
    streamer = Streamer(credentials)
    streamer.read(lambda tweet: sys.stdout.write(tweet.text+'\n'), terms, quantity, center, distance)
#    writer = CSVWriter()
#    writer.fopen(filename)
#    streamer.read(terms, lambda tweet: writer.write(["0", tweet.text])), quantity, center, distance)
#    writer.close()

except Exception as e:
    print 'Error: %r' % e

