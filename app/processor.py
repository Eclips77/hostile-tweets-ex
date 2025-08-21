import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import pandas

# nltk.download('vader_lexicon')
# tweet = 'Skillcate is a great Youtube Channel to learn Data Science'
# score = SentimentIntensityAnalyzer().polarity_scores(tweet)
# print(score)

class TweetsProcessor:
    """
    a processing class for tweets data
    """
    def __init__(self):
        pass