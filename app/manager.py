from app.fetcher import FetcherDal
from app.processor import TweetsProcessor
import json

class TweetProcessingManager:
    """
    manager class of the dal and processing classes
    """
    
    def __init__(self):
        self.fetcher = FetcherDal()
        self.processor = None
    
    def process_all_tweets(self):
        """
        procssing all the tweets from the db
        """
        dataframe = self.fetcher.fetch_all_tweets()
        
        if dataframe.empty:
            return {"error": "No tweets found"}
        
        self.processor = TweetsProcessor(dataframe)
        results = []
        
        for index, row in dataframe.iterrows():
            text = str(row.get("Text", ""))
            tweet_id = str(row.get("_id", f"tweet_{index}"))
            
            result = self.processor.process_single_tweet(text, tweet_id)
            results.append(result)
        
        self.fetcher.close_connection()
        
        return results
    
 


if __name__ == "__main__":
    manager = TweetProcessingManager()
    
    # all_results = manager.process_all_tweets()
    # print(json.dumps(all_results, indent=2))

