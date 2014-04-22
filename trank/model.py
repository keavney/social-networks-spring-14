import sys

from nltk.tokenize import wordpunct_tokenize
import re
import nltk

class Record:
    def __init__(self,label,message,followers):
        self.label = label
        self.message = message
        self.followers = followers
        self.features_set = {}              # Dictionary used by classifier
        self.hashtags = []                  # Words marked by hashtags
        self.probability = 0.0              # Relevance to the label '1'
        self.impact_score = 0.0             # Probability * (followers + 1)
        
        # Get set of unique words contained in a tweet
        self.message_words = set(wordpunct_tokenize(self.message.replace('\r',' ').lower()))
        
        # Get rid of punctuation,tokens,numbers, and single letters.
        self.message_words = [w for w in self.message_words if re.search('[a-zA-Z]', w) and len(w) > 1]

    # Generate a tweet's features_set according to input features
    def get_features_set(self,features_set):
        for k,v in features_set.items():
            if k in self.message_words:
                self.features_set[k] = 1
            else:
                self.features_set[k] = 0

def get_record_list_from_csv_filename(csvfilename, delim):
    records_list = []
    with open(csvfilename, 'rb') as csvfile:
        for line in csvfile.readlines():
            fields = line.split(delim)
            if len(fields) == 3:
                record = Record(fields[0],fields[1],fields[2])
                records_list.append(record)
    return records_list

def create_model_from_csv_filename(csvfilename, delim, min_frequency=3):
    # Read csv file, create records list
    records_list = get_record_list_from_csv_filename(csvfilename, delim)

    # Get word count from all messages
    word_counts = {}
    for record in records_list:
        for word in record.message_words:
            if word in word_counts:
                word_counts[word] += 1
            else:
                word_counts[word] = 1
    
    # Filter out words that don't qualify
    filtered_word_counts = {}
    nonsense_words = ['and','the','http','co']
    for k, v in word_counts.items():
        if v > min_frequency and k not in nonsense_words:
            filtered_word_counts[k] = v
    
    # Create training model from record feature sets
    training_model = []
    for record in records_list:
        record.get_features_set(filtered_word_counts)
        training_model.append((record.features_set, record.label))
    
    return training_model

