import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import re
from collections import Counter
from models.process_data_model import ProcessTweet
class TweetsProcessor:
    """
    a processing class for tweets data
    """
    def __init__(self,dataframe,column="Text"):
        self.df = dataframe
        self.message_column = column

    def _find_rarest_word(self, text: str) -> str:
        """
        find the rarest word in a tweet       
        Args:
            text: tweet text
            
        Returns:
                most rarest word
        """
        if not text:
            return ""
        words = re.findall(r'\b\w+\b', text.lower())
        if not words:
            return ""
        word_count = Counter(words)
        rarest_word = min(word_count.keys(), key=lambda x: (word_count[x], words.index(x)))
        return rarest_word

    def _get_sentiments(self):
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
        
    def _extract_weapon_names(self) -> str:
        with open('data.weapons.txt', 'r') as file:
            weaponsList = {line.strip() for line in file}
        matches = []
        all_words = ' '.join(self.df[self.message_column].dropna()).split()
        for item in all_words:
            if item.lower() in weaponsList:
                matches.append(item)
        return matches[0]

    def analyze_dataframe(self, df, text_column: str = 'text'):
        """
        Analyze Twitter tweets DataFrame
        
        Args:
            df: DataFrame with tweets
            text_column: Name of the column containing the text (default: 'text')
            
        Returns:
            List of dictionaries with processed data
        """
        if text_column not in df.columns:
            raise ValueError(f"Column '{text_column}' not found in DataFrame")
        
        results = []
        
        for index, row in df.iterrows():
            original_text = str(row[text_column]) if row[text_column] is not None else ""
            
            rarest_word = self._find_rarest_word(original_text)
            sentiment = self._get_sentiments()
            weapons_list = self._extract_weapon_names()
            result_dict = ProcessTweet(
                original_text= original_text,
                rarest_word= rarest_word,
                sentiment= sentiment,
                weapons_detected= weapons_list
            )
            
            results.append(result_dict)
        
        return results
