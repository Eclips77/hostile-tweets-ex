from typing import Optional
from uuid import uuid4

class ProcessTweet:
    """
    Document class representing a tweet with data information
    """
    
    def __init__(self, original_text: Optional[str] = None, rarest_word: Optional[str] = None, sentiment: Optional[str] = None, weapons_detected: Optional[str] = None, tweet_id: Optional[str] = None):
        """
        Initialize a new Document instance
        
        Args:
            original_text (str): Original text of the tweet
            rarest_word (str): Rarest word of the tweet
            sentiment (str): Sentiment of the tweet
            weapons_detected (str): Weapons detected in the tweet
            doc_id (Optional[str]): Document ID, auto-generated if not provided
        """
        self.id = tweet_id if tweet_id else str(uuid4())
        self.original_text = original_text
        self.rarest_word = rarest_word
        self.sentiment = sentiment
        self.weapons_detected = weapons_detected

    def to_dict(self) -> dict:
            """
            Convert document to dictionary format
            
            Returns:
                dict: Document as dictionary
            """
            return {
                "id": self.id,
                "original_text": self.original_text,
                "rarest_word": self.rarest_word,
                "sentiment": self.sentiment,
                "weapons_detected": self.weapons_detected
            } 
    
    @classmethod
    def from_dict(cls, data: dict):
        """
        Create Document instance from dictionary
        
        Args:
            data (dict): Dictionary containing document data
            
        Returns:
            Document: New Document instance
        """
        return cls(
            original_text=data.get("original_text"),
            rarest_word=data.get("rarest_word"),
            sentiment=data.get("sentiment"),
            weapons_detected=data.get("weapons_detected"),
            tweet_id=data.get("id")
        )      