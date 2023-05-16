from transformers import pipeline
import json
# import nltk
# from nltk.corpus import stopwords
# from nltk.tokenize import word_tokenize
import re

# nltk.download('stopwords')
# nltk.download('punkt')

models = ["textattack/roberta-base-imdb", "textattack/roberta-base-rotten-tomatoes",
          "finiteautomata/bertweet-base-sentiment-analysis"]
sentiment_analysis = pipeline("sentiment-analysis", model=models[2])

# Recursive function to search for quotes in a nested data structure


def find_quotes(data, quotes_list):
    if isinstance(data, dict):
        # If the data is a dictionary, search each value for quotes
        for key, value in data.items():
            # If the key is a string, add it to the quotes list
            if isinstance(key, str):
                quotes_list.append(key)
            find_quotes(value, quotes_list)
    elif isinstance(data, list):
        # If the data is a list, search each element for quotes
        for element in data:
            find_quotes(element, quotes_list)
    elif isinstance(data, str):
        # If the data is a string, add it to the quotes list
        quotes_list.append(data)


# Read data from JSON file
with open('sample.json', 'r') as f:
    data = json.load(f)

# Initialize an empty list to hold the quotes
quotes_list = []

# Remove >128
# my_list = [s for s in quotes_list if len(s) <= 128]

# Search for quotes in the data structure
find_quotes(data, quotes_list)

# stop_words = set(stopwords.words('english'))

def filter_sent(sentence):
    # word_tokens = word_tokenize(sentence)
    # filtered_sentence = [w for w in word_tokens if not w.lower() in stop_words]
    # filtered_sentence = " ".join(filtered_sentence)
    # print(filtered_sentence)
    filtered_sentence = re.sub("[^A-Za-z0-9 ]", "", sentence)
    return filtered_sentence


quotes_list = [filter_sent(q) for q in quotes_list]

def get_emotion(text):
    acc = 0
    count = int(len(text) / 128) + 1
    pos = [0, 0]
    neg = [0, 0]
    for i in range(count):
        start = int(128 * i)
        end = min(int(128 * (i + 1)), len(text))
        # print(start, end)
        result = sentiment_analysis(text[start:end])[0]
        # print(result)
        if result['label'] == 'POS':
            acc += result['score']
            pos[0] += result['score']
            pos[1] += 1
        elif result['label'] == 'NEG':
            acc -= result['score']
            neg[0] += result['score']
            neg[1] += 1

    if acc == 0:
        return 'NEU', acc
    elif acc > 0:
        return 'POS', pos[0] / pos[1]
    else:
        return 'NEG', neg[0] / neg[1]

quote_dict = {}
for text in quotes_list:
    label, score = get_emotion(text)
    # print(f"Sentiment: {label}, Score: {score}\n")
    quote_dict[f"{text}"] = (label, score)

with open("quote_sentiment.json", "w") as f:
    json.dump(quote_dict, f)


# quote_dict = {}

# for text in quotes_list:
#     result = sentiment_analysis(text)[0]
#     quote_dict[text] = (result['label'], result['score'])

# for key, value in quote_dict.items():
#     print(key + ' ---> ' + str(value) + "\n\n")

# print(text)
# print(f"Sentiment: {result['label']}, Score: {result['score']}\n")
