from transformers import pipeline

sentiment_analysis = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")

text = "I love this movie! It's so entertaining and funny."
result = sentiment_analysis(text)[0]

print(f"Sentiment: {result['label']}, Score: {result['score']}")