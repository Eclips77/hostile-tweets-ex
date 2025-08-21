import os

USER = os.getenv("MONGO_USER", "IRGC")
PASSWORD = os.getenv("MONGO_PASSWORD", "iraniraniran")
DB_NAME = os.getenv("MONGO_DB_NAME", "IranMalDB")
CONNECTION_STRING = os.getenv("MONGO_CONNECTION_STRING", "mongodb+srv://IRGC:iraniraniran@iranmaldb.gurutam.mongodb.net/")