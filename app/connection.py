from pymongo import MongoClient
from pymongo.database import Database
from data import config

class DatabaseConnection:
    """
    MongoDB connection manager
    """
    
    def __init__(self):
        """
        Initialize database connection
        """
        self.client = None
        self.database = None
    
    def connect(self) -> Database:
        """
        Establish connection to MongoDB Atlas
        
        Returns:
            Database: MongoDB database instance
        """
        try:
            self.client = MongoClient(config.CONNECTION_STRING)
            self.database = self.client[config.DB_NAME]
            return self.database
        except Exception as e:
            raise ConnectionError(f"Failed to connect to MongoDB: {e}")
    
    def disconnect(self):
        """
        Close database connection
        """
        if self.client:
            self.client.close()