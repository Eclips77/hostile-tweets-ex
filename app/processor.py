import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import pandas
from collections import Counter
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

    def get_sentiments(self):
        """
        Analyze the sentiments of the tweets in the dataframe.
        """
        nltk.download('vader_lexicon')
        sia = SentimentIntensityAnalyzer()
        
        self.df['Sentiment'] = self.df[self.message_column].apply(lambda x: sia.polarity_scores(x))
        
        self.df['Compound'] = self.df['Sentiment'].apply(lambda x: x['compound'])
        self.df['Sentiment_Label'] = self.df['Compound'].apply(self._classify_sentiment)
        
        return self.df['Sentiment'].todict()
    
    def _classify_sentiment(self, compound_score)-> str:
        """
        Classify sentiment based on compound score.

        Returns: a sens tag by score.
        """
        if compound_score >= 0.5:
            return "positive"
        elif compound_score <= -0.5:
            return "negative text"
        else:
            return "neutral text"
        
    def extract_weapon_names(self):
        pass