# Tweet Processing API with Detailed Logging

## Overview
This API processes tweets with malicious content detection, sentiment analysis, and weapons detection. The system includes comprehensive logging for debugging and monitoring.

## Features
- **Automatic Processing**: Processes all tweets when server starts
- **Sentiment Analysis**: Uses VADER sentiment analyzer
- **Weapons Detection**: Detects weapons mentioned in tweets
- **Rarest Word Detection**: Finds the rarest word in each tweet
- **Comprehensive Logging**: Detailed logs for debugging and monitoring

## API Endpoints

### 1. Health Check
```
GET /
```
Returns server status

### 2. Get Processed Tweets
```
GET /api/processed-tweets
```
Returns JSON array of all processed tweets with analysis results

Example response:
```json
[
  {
    "id": "tweet_123",
    "rarest_word": "example",
    "sentiment": "negative",
    "original_text": "Sample tweet text",
    "weapons_detected": "knife, gun"
  }
]
```

## Running the API

### Method 1: Using run_api.py
```bash
python run_api.py
```

### Method 2: Direct uvicorn command
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

## Logging

The system generates detailed logs in multiple levels:
- **INFO**: General operation information
- **DEBUG**: Detailed processing steps
- **WARNING**: Non-critical issues
- **ERROR**: Errors with full traceback

### Log Output Locations:
1. **Console**: Real-time logs displayed in terminal
2. **File**: Logs saved to `tweet_processing.log`

### Log Format:
```
TIMESTAMP - MODULE_NAME - LEVEL - MESSAGE
```

## Log Messages You'll See:

### Manager Logs:
- "Initializing TweetProcessingManager..."
- "Starting process_all_tweets method..."
- "Successfully processed X/Y tweets"

### Fetcher Logs:
- "Initializing FetcherDal..."
- "Connected to database successfully"
- "Successfully retrieved X documents from MongoDB"

### Processor Logs:
- "Initializing TweetsProcessor..."
- "Loaded X weapons from weapons.txt"
- "Processing single tweet with ID: X"

## Troubleshooting

### Common Issues and Log Messages:

1. **Database Connection Issues**
   - Look for: "Failed to initialize FetcherDal"
   - Check MongoDB connection settings

2. **Empty Database**
   - Look for: "No tweets found in database"
   - Verify data exists in MongoDB collection

3. **Missing Weapons File**
   - Look for: "Weapons file not found at path"
   - Ensure `data/weapons.txt` exists

4. **Sentiment Analysis Issues**
   - Look for: "Could not initialize sentiment analyzer"
   - Check NLTK installation and internet connection

5. **Processing Errors**
   - Look for: "Failed to process tweet at index X"
   - Individual tweet processing errors (processing continues)

## Dependencies
- FastAPI
- Uvicorn
- MongoDB
- Pandas
- NLTK
- PyMongo

## File Structure
```
├── app/
│   ├── main.py          # FastAPI application with logging
│   ├── manager.py       # Processing manager with detailed logs
│   ├── fetcher.py       # Database fetcher with connection logs
│   ├── processor.py     # Tweet processor with analysis logs
│   └── connection.py    # Database connection
├── data/
│   ├── weapons.txt      # Weapons list for detection
│   └── config.py        # Configuration settings
├── run_api.py           # Server startup script
└── tweet_processing.log # Log file (created automatically)
```

## Monitoring
Monitor the logs to track:
- Processing performance
- Error frequency
- Database connection health
- Individual tweet processing status
