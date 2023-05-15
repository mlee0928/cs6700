from transformers import pipeline
import json

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
my_list = [s for s in quotes_list if len(s) <= 128]

# Search for quotes in the data structure
find_quotes(data, quotes_list)

for text in quotes_list[1:7]:
    result = sentiment_analysis(text)[0]
    print(text)
    print(f"Sentiment: {result['label']}, Score: {result['score']}\n")


# quote_dict = {}

# for text in quotes_list:
#     result = sentiment_analysis(text)[0]
#     quote_dict[text] = (result['label'], result['score'])

# for key, value in quote_dict.items():
#     print(key + ' ---> ' + str(value) + "\n\n")

# print(text)
# print(f"Sentiment: {result['label']}, Score: {result['score']}\n")
