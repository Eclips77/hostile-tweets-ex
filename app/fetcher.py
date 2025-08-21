from app.connection import DatabaseConnection
from typing import Optional
from data import config
import logging
import pandas as pd

logger = logging.getLogger(__name__)

class FetcherDal:
    """Data Access Layer for fetching tweet data from mongodb"""
    
    def __init__(self):
        """Initialize DAL with database connection"""
        logger.info("Initializing FetcherDal...")
        try:
            self.connection = DatabaseConnection()
            logger.info("DatabaseConnection object created successfully")
            
            self.database = self.connection.connect()
            logger.info(f"Connected to database successfully")
            
            self.collection = self.database[config.MONGODB_COLLECTION]
            logger.info(f"Connected to collection: {config.MONGODB_COLLECTION}")
            
        except Exception as e:
            logger.error(f"Failed to initialize FetcherDal: {str(e)}")
            logger.error(f"Error type: {type(e).__name__}")
            logger.error("Full traceback:", exc_info=True)
            raise
    
    def fetch_all_tweets(self) -> pd.DataFrame:
        """
        Get all tweets from the database with detailed logging
        
        Returns:
            DataFrame of all tweets or empty DataFrame on error
        """
        logger.info("Starting to fetch all tweets from database...")
        
        try:
            # Execute the database query
            logger.debug("Executing MongoDB find query...")
            results = self.collection.find({}, {"_id": 0})
            
            # Convert to list for counting and DataFrame creation
            logger.debug("Converting MongoDB cursor to list...")
            documents = [doc for doc in results]
            document_count = len(documents)
            
            logger.info(f"Successfully retrieved {document_count} documents from MongoDB")
            
            if document_count == 0:
                logger.warning("No documents found in the collection")
                return pd.DataFrame()
            
            # Create DataFrame
            logger.debug("Creating pandas DataFrame from documents...")
            dataframe = pd.DataFrame(documents)
            
            logger.info(f"Successfully created DataFrame with shape: {dataframe.shape}")
            logger.info(f"DataFrame columns: {list(dataframe.columns)}")
            
            return dataframe
            
        except Exception as e:
            logger.error(f"Error getting all tweets: {str(e)}")
            logger.error(f"Error type: {type(e).__name__}")
            logger.error("Full traceback:", exc_info=True)
            return pd.DataFrame()

    def close_connection(self):
        """
        Close database connection with detailed logging
        """
        logger.info("Attempting to close database connection...")
        
        try:
            if hasattr(self, 'connection') and self.connection:
                self.connection.disconnect()
                logger.info("Database connection closed successfully")
            else:
                logger.warning("No connection object found or connection already closed")
                
        except Exception as e:
            logger.error(f"Failed to close database connection: {str(e)}")
            logger.error(f"Error type: {type(e).__name__}")
            logger.error("Full traceback:", exc_info=True)


# if __name__ == "__main__":
#     dal = FetcherDal()
#     x = dal.fetch_all_tweets()
#     print(x.head(10))