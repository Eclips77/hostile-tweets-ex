# Tweet Processing Manager

מנג'ר מתקדם לעיבוד וניתוח ציוצים (tweets) המיועד לשימוש עם API.

## תכונות

### 🎯 **תכונות עיקריות:**
- **שליפת נתונים:** חיבור לבסיס נתונים MongoDB ושליפת tweets
- **עיבוד טקסט:** ניתוח sentiment, מציאת מילים נדירות וזיהוי נשקים
- **ביצועים מותאמים:** עיבוד יעיל עם caching ואתחול חכם
- **תמיכה ב-API:** מתודות מותאמות לשימוש ב-REST API
- **Logging מפורט:** מעקב אחר כל הפעולות
- **Context Manager:** ניהול אוטומטי של חיבורים

### 🔧 **מתודות זמינות:**

#### מתודות עיקריות:
- `process_all_tweets()` - עיבוד כל הטוויטים מבסיס הנתונים
- `process_single_tweet_text(text)` - עיבוד טקסט בודד (לא דורש DB)
- `process_tweet_batch(texts)` - עיבוד מספר טקסטים במקביל
- `analyze_tweets(dataframe)` - עיבוד DataFrame קיים

#### מתודות עזר:
- `fetch_tweets()` - שליפת נתונים מהדאטאבייס
- `get_processing_stats()` - סטטיסטיקות על המעבד
- `clear_cache()` - ניקוי זיכרון זמני
- `close_connections()` - סגירת חיבורים

## דוגמאות שימוש

### 1. עיבוד טקסט בודד (מושלם ל-API endpoint)

```python
from app.manager import TweetProcessingManager

# יצירת מנג'ר
with TweetProcessingManager() as manager:
    result = manager.process_single_tweet_text("I love this beautiful day!")
    print(result)
    # Output: {
    #   "id": "uuid...",
    #   "original_text": "I love this beautiful day!",
    #   "sentiment": "positive",
    #   "rarest_word": "beautiful",
    #   "weapons_detected": "none"
    # }
```

### 2. עיבוד batch של טקסטים

```python
texts = [
    "Great day today!",
    "I hate this situation",
    "The soldier had a rifle"
]

with TweetProcessingManager() as manager:
    results = manager.process_tweet_batch(texts)
    for result in results:
        print(f"Sentiment: {result['sentiment']}")
```

### 3. עיבוד כל הנתונים מהדאטאבייס

```python
with TweetProcessingManager() as manager:
    results = manager.process_all_tweets()
    print(f"Processed {len(results)} tweets")
```

### 4. שימוש עם custom DataFrame

```python
import pandas as pd

df = pd.DataFrame({
    'Text': ['Tweet 1', 'Tweet 2', 'Tweet 3'],
    '_id': ['id1', 'id2', 'id3']
})

with TweetProcessingManager(text_column="Text") as manager:
    results = manager.analyze_tweets(df)
```

## התקנה ודרישות

### דרישות:
```
pandas
nltk
pymongo
```

### הגדרת קונפיגורציה:
וודא שקובץ `data/config.py` מכיל:
```python
MONGODB_CONNECTION_STRING = "your_mongodb_connection"
MONGODB_DATABASE = "your_database_name"
MONGODB_COLLECTION = "your_collection_name"
```

### קובץ נשקים:
וודא שקיים קובץ `data/weapons.txt` עם רשימת נשקים (כל נשק בשורה נפרדה).

## שימוש עם API Framework

### Flask דוגמא:

```python
from flask import Flask, request, jsonify
from app.manager import TweetProcessingManager

app = Flask(__name__)
manager = TweetProcessingManager()

@app.route('/analyze', methods=['POST'])
def analyze_tweet():
    data = request.json
    text = data.get('text', '')
    
    try:
        result = manager.process_single_tweet_text(text)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/analyze_batch', methods=['POST'])
def analyze_batch():
    data = request.json
    texts = data.get('texts', [])
    
    try:
        results = manager.process_tweet_batch(texts)
        return jsonify(results)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
```

### FastAPI דוגמא:

```python
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from app.manager import TweetProcessingManager

app = FastAPI()
manager = TweetProcessingManager()

class TweetRequest(BaseModel):
    text: str

class BatchRequest(BaseModel):
    texts: List[str]

@app.post("/analyze")
async def analyze_tweet(request: TweetRequest):
    result = manager.process_single_tweet_text(request.text)
    return result

@app.post("/analyze_batch")
async def analyze_batch(request: BatchRequest):
    results = manager.process_tweet_batch(request.texts)
    return results
```

## פורמט התוצאות

כל תוצאה מכילה:

```python
{
    "id": "unique_identifier",
    "original_text": "הטקסט המקורי",
    "sentiment": "positive/negative/neutral/unknown",
    "rarest_word": "המילה הכי נדירה",
    "weapons_detected": "רשימת נשקים שנמצאו או 'none'"
}
```

## טיפים לביצועים

1. **השתמש ב-Context Manager:** תמיד השתמש ב-`with` כדי לוודא סגירת חיבורים
2. **Caching:** המנג'ר שומר נתונים בזיכרון - השתמש ב-`clear_cache()` אם נדרש
3. **Batch Processing:** עדיף לעבד טקסטים במקבצים מאשר אחד אחד
4. **Error Handling:** המנג'ר זורק exceptions מפורטות - תפוס אותן

## Logging

המנג'ר משתמש ב-Python logging. כדי לראות logs:

```python
import logging
logging.basicConfig(level=logging.INFO)
```

## תמיכה וטיפול בשגיאות

המנג'ר מטפל בשגיאות הבאות:
- חיבור כושל לדאטאבייס
- קובץ נשקים חסר
- עמודות חסרות ב-DataFrame
- טקסט ריק או לא תקין
- שגיאות בעיבוד sentiment

כל השגיאות נרשמות ב-log ונזרקות כ-exceptions עם הודעות ברורות.
