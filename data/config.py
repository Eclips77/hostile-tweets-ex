import os

MONGO_USER = os.getenv("MONGO_USER", "IRGC")
MONGO_PASSWORD = os.getenv("MONGO_PASSWORD", "iraniraniran")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "IranMalDB")
MONGO_CONNECTION_STRING = os.getenv("MONGO_CONNECTION_STRING", "mongodb+srv://IRGC:iraniraniran@iranmaldb.gurutam.mongodb.net/")
MONGODB_COLLECTION = os.getenv("MONGODB_COLLECTION","tweets")