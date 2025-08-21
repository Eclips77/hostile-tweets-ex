from pymongo import MongoClient
from pymongo.database import Database
from data import config
import logging

logger = logging.getLogger(__name__)

class DatabaseConnection:
    """
    MongoDB connection manager with improved error handling and timeouts
    """
    
    def __init__(self):
        """
        Initialize database connection
        """
        self.client = None
        self.database = None
    
    def connect(self) -> Database:
        """
        Establish connection to MongoDB Atlas with timeout and retry logic
        
        Returns:
            Database: MongoDB database instance
        """
        logger.info("Attempting to connect to MongoDB Atlas...")
        
        try:
            # Create MongoClient with proper timeouts and connection settings
            self.client = MongoClient(
                config.MONGO_CONNECTION_STRING,
                serverSelectionTimeoutMS=5000,  # 5 seconds
                connectTimeoutMS=10000,         # 10 seconds
                socketTimeoutMS=20000,          # 20 seconds
                maxPoolSize=10,
                retryWrites=True
            )
            
            # Test the connection
            logger.info("Testing MongoDB connection...")
            self.client.admin.command('ping')
            logger.info("MongoDB connection successful")
            
            # Connect to the specific database
            self.database = self.client[config.MONGO_DB_NAME]
            logger.info(f"Connected to database: {config.MONGO_DB_NAME}")
            
            return self.database
            
        except Exception as e:
            logger.error(f"Failed to connect to MongoDB Atlas: {str(e)}")
            logger.error(f"Connection string: {config.MONGO_CONNECTION_STRING[:20]}...")
            logger.error(f"Database name: {config.MONGO_DB_NAME}")
            raise ConnectionError(f"Failed to connect to MongoDB: {e}")
    
    def disconnect(self):
        """
        Close database connection safely
        """
        logger.info("Closing MongoDB connection...")
        try:
            if self.client:
                self.client.close()
                logger.info("MongoDB connection closed successfully")
        except Exception as e:
            logger.error(f"Error closing MongoDB connection: {str(e)}")