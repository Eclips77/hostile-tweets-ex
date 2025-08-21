from app.connection import DatabaseConnection
from typing import List, Optional
from data import config

class FetcherDal:
    """Data Access Layer for fetching tweet data from mongodb ."""
    def __init__(self):
        """ 
        Initialize DAL with database connection
        """
        self.connection = DatabaseConnection()
        self.database = self.connection.connect()
        self.collection = self.database[config.MONGODB_COLLECTION]
    
    def fetch_all_tweets(self):
        pass