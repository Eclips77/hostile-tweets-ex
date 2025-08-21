from app.connection import DatabaseConnection
from typing import List, Optional
from data import config
import logging

class FetcherDal:
    """Data Access Layer for fetching tweet data from mongodb ."""
    def __init__(self):
        """ 
        Initialize DAL with database connection
        """
        self.connection = DatabaseConnection()
        self.database = self.connection.connect()
        self.collection = self.database[config.MONGODB_COLLECTION]
    
    def fetch_all_tweets(self)-> list:
        """
        Get all tweets from the database
        
        Returns:
            List of all tweets
        """
        try:
            results = self.collection.find({},{"_id":0})
            return [doc for doc in results]
        except Exception as e:
            print(f"Error getting all tweets: {e}")
            return []

    def close_connection(self):
        """
        Close database connection
        """
        self.connection.disconnect()



# if __name__ == "__main__":
#     dal = FetcherDal()
#     x = dal.fetch_all_tweets()
#     print(len(x))
    