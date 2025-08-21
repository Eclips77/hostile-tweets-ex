from fastapi import FastAPI, HTTPException
from app.manager import TweetProcessingManager
import logging

app = FastAPI(title="Malicious Text Feature Engineering System", version="1.0.0")
manager = TweetProcessingManager()
processed_data = None

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.on_event("startup")
async def startup_event():
    """Automatically process all tweets when server starts"""
    global processed_data
    logger.info("Starting automatic tweet processing...")
    try:
        processed_data = manager.process_all_tweets()
        logger.info(f"Successfully processed {len(processed_data) if isinstance(processed_data, list) else 0} tweets")
    except Exception as e:
        logger.error(f"Error during startup processing: {e}")
        processed_data = {"error": f"Failed to process tweets: {str(e)}"}

@app.get("/api/processed-tweets")
async def get_processed_tweets():
    """Returns the JSON of processed tweets data"""
    if processed_data is None:
        raise HTTPException(status_code=503, detail="Data processing not completed yet")
    
    return processed_data

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"status": "active"}

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run("app.main:app", host="0.0.0.0", port=8000)