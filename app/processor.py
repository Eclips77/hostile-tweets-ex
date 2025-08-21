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

    def most_rare_word(self,row):
        words = row.str.cat(sep=' ').split()  
        word_counts = Counter(words) 
        min_count = min(word_counts.values())
        rare_words = [word for word, count in word_counts.items() if count == min_count]
        return rare_words

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
        with open('data.weapons.txt', 'r') as file:
            weaponsList = {line.strip() for line in file}
        matches = []
        all_words = ' '.join(self.df[self.message_column].dropna()).split()
        for item in all_words:
            if item.lower() in weaponsList:
                matches.append(item)
        return matches