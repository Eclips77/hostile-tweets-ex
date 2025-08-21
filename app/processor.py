import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import pandas
from collections import Counter

# nltk.download('vader_lexicon')
# tweet = 'Skillcate is a great Youtube Channel to learn Data Science'
# score = SentimentIntensityAnalyzer().polarity_scores(tweet)
# print(score)

class TweetsProcessor:
    """
    a processing class for tweets data
    """
    def __init__(self,dataframe,column="Text"):
        self.df = dataframe
        self.message_column = column

    def get_most_common_words(self,top_n=1) -> dict:
        """Returns a dictionary containing the  most common word in the tweets column.
        This method concatenates all the tweets, splits them into words, counts their occurrences,
        and returns the top N most common words.
        Args:
            top_n (int): The number of most common words to return. Default is 1.
        """
            
        all_words = ' '.join(self.df[self.message_column].dropna())
        word_counts = Counter(all_words.split())
        return dict(word_counts.most_common(top_n))