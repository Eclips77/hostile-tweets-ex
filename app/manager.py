from regex import F
from app.fetcher import FetcherDal
from app.processor import TweetsProcessor
# import pandas as pd


fetcher = FetcherDal()
db = fetcher.fetch_all_tweets()
processor = TweetsProcessor(db)

c = processor.analyze_dataframe()
print(c)