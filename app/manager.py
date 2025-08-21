from app.fetcher import FetcherDal
from app.processor import TweetsProcessor
import json
import logging

# Configure logging for this module
logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()  # Only console logging to avoid permission issues in containers
    ]
)

class TweetProcessingManager:
    """
    manager class of the dal and processing classes
    """
    
    def __init__(self):
        """Initialize TweetProcessingManager with fetcher and processor components"""
        logger.info("Initializing TweetProcessingManager...")
        try:
            self.fetcher = FetcherDal()
            self.processor = None
            logger.info("TweetProcessingManager initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize TweetProcessingManager: {str(e)}")
            logger.error(f"Error type: {type(e).__name__}")
            raise
    
    def process_all_tweets(self):
        """
        Processing all the tweets from the database with detailed logging
        Returns: List of processed tweet dictionaries or error dictionary
        """
        logger.info("Starting process_all_tweets method...")
        
        try:
            # Step 1: Fetch tweets from database
            logger.info("Fetching tweets from database...")
            dataframe = self.fetcher.fetch_all_tweets()
            logger.info(f"Successfully fetched {len(dataframe)} tweets from database")
            
            # Step 2: Check if dataframe is empty
            if dataframe.empty:
                logger.warning("No tweets found in database - returning error response")
                return {"error": "No tweets found"}
            
            # Step 3: Initialize processor
            logger.info("Initializing TweetsProcessor with fetched dataframe...")
            try:
                self.processor = TweetsProcessor(dataframe)
                logger.info("TweetsProcessor initialized successfully")
            except Exception as e:
                logger.error(f"Failed to initialize TweetsProcessor: {str(e)}")
                logger.error(f"Error type: {type(e).__name__}")
                raise
            
            # Step 4: Process each tweet
            results = []
            total_tweets = len(dataframe)
            logger.info(f"Starting to process {total_tweets} tweets individually...")
            
            for idx, (index, row) in enumerate(dataframe.iterrows()):
                try:
                    text = str(row.get("Text", ""))
                    tweet_id = str(row.get("_id", f"tweet_{idx}"))
                    
                    logger.debug(f"Processing tweet {idx + 1}/{total_tweets} with ID: {tweet_id}")
                    
                    if not text.strip():
                        logger.warning(f"Tweet {tweet_id} has empty text content")
                    
                    result = self.processor.process_single_tweet(text, tweet_id)
                    results.append(result)
                    
                    if (idx + 1) % 100 == 0:  # Log progress every 100 tweets
                        logger.info(f"Processed {idx + 1}/{total_tweets} tweets")
                        
                except Exception as e:
                    logger.error(f"Failed to process tweet at index {idx}: {str(e)}")
                    logger.error(f"Tweet ID: {row.get('_id', 'Unknown')}")
                    logger.error(f"Error type: {type(e).__name__}")
                    # Continue processing other tweets instead of failing completely
                    continue
            
            # Step 5: Close database connection
            logger.info("Closing database connection...")
            try:
                self.fetcher.close_connection()
                logger.info("Database connection closed successfully")
            except Exception as e:
                logger.error(f"Failed to close database connection: {str(e)}")
                logger.error(f"Error type: {type(e).__name__}")
            
            # Step 6: Return results
            successful_results = len(results)
            logger.info(f"Successfully processed {successful_results}/{total_tweets} tweets")
            
            if successful_results == 0:
                logger.error("No tweets were successfully processed")
                return {"error": "Failed to process any tweets"}
            
            return results
            
        except Exception as e:
            logger.error(f"Critical error in process_all_tweets: {str(e)}")
            logger.error(f"Error type: {type(e).__name__}")
            logger.error("Full traceback:", exc_info=True)
            
            # Ensure database connection is closed even on error
            try:
                if hasattr(self, 'fetcher') and self.fetcher:
                    self.fetcher.close_connection()
                    logger.info("Database connection closed after error")
            except Exception as cleanup_error:
                logger.error(f"Failed to close database connection during cleanup: {str(cleanup_error)}")
            
            return {"error": f"Processing failed: {str(e)}"}
    
 


if __name__ == "__main__":
    manager = TweetProcessingManager()
    
    # all_results = manager.process_all_tweets()
    # print(json.dumps(all_results, indent=2))

