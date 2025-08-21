FROM python:3.11-slim
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

ENV NLTK_DATA=/usr/local/share/nltk_data
RUN mkdir -p "$NLTK_DATA" && \
    python -c "import nltk; nltk.download('vader_lexicon', download_dir='$NLTK_DATA'); nltk.download('punkt', download_dir='$NLTK_DATA')" && \
    chmod -R 755 "$NLTK_DATA"

COPY app ./app
COPY data/ ./data

EXPOSE 8000
CMD ["python","-m","uvicorn","app.main:app","--host","0.0.0.0","--port","8000"]
