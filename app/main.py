from fastapi import FastAPI,HTTPException
from app.manager import TweetProcessingManager

app = FastAPI(title="Malicious Text Feature Engineering System",version="1.0.0")

