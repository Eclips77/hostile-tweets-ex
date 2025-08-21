import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import re
import os
from collections import Counter
from typing import Dict, Optional
import uuid
class TweetsProcessor:
    """
    a processing class for tweets data
    """
    def __init__(self, dataframe, column="Text"):
        self.df = dataframe
        self.message_column = column
        self.weapons_set = self._load_weapons_list()
        self.sia = self._initialize_sentiment_analyzer()

    def _load_weapons_list(self):
        """Load weapons list from file once during initialization"""
        weapons_file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'weapons.txt')
        try:
            with open(weapons_file_path, 'r') as file:
                return {line.strip().lower() for line in file if line.strip()}
        except FileNotFoundError:
            print(f"Warning: Weapons file not found at {weapons_file_path}")
            return set()
    
    def _initialize_sentiment_analyzer(self):
        """Initialize sentiment analyzer once during initialization"""
        try:
            nltk.download('vader_lexicon', quiet=True)
            return SentimentIntensityAnalyzer()
        except Exception as e:
            print(f"Warning: Could not initialize sentiment analyzer: {e}")
            return None

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

    def _get_sentiment_for_text(self, text: str) -> str:
        """
        Analyze the sentiment of a single text.
        
        Args:
            text: The text to analyze
            
        Returns:
            Sentiment label (positive/negative/neutral)
        """
        if not self.sia or not text:
            return "unknown"
        
        scores = self.sia.polarity_scores(text)
        compound_score = scores['compound']
        return self._classify_sentiment(compound_score)
    
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
        
    def _extract_weapons_from_text(self, text: str) -> list:
        """
        Extract weapon names (single or multi-word) from text.
        """
        if not text or not self.weapons_set:
            return []
        
        text_lower = text.lower()
        found_weapons = {weapon.lower() for weapon in self.weapons_set if weapon in text_lower}
        return list(found_weapons)

    def process_single_tweet(self, text: str, tweet_id: Optional[str] = None) -> Dict:
        """
        Process a single tweet text and return analysis results.
        
        Args:
            text: Tweet text to analyze
            tweet_id: Optional tweet ID
            
        Returns:
            Dictionary containing analysis results
        """
        if not text:
            text = ""
        
        rarest_word = self._find_rarest_word(text)
        sentiment = self._get_sentiment_for_text(text)
        weapons_list = self._extract_weapons_from_text(text)
        weapons_str = ", ".join(weapons_list) if weapons_list else "none"
        
        return {
            "id": tweet_id or str(uuid.uuid4()),
            "rarest_word": rarest_word,
            "sentiment": sentiment,
            "original_text": text,
            "weapons_detected": weapons_str
        }
