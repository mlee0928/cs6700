import json
import re

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


def filter_sent(sentence):
    # word_tokens = word_tokenize(sentence)
    # filtered_sentence = [w for w in word_tokens if not w.lower() in stop_words]
    # filtered_sentence = " ".join(filtered_sentence)
    # print(filtered_sentence)
    filtered_sentence = re.sub("[^A-Za-z0-9 ]", "", sentence)
    return filtered_sentence


# Read data from JSON file
with open('sample.json', 'r') as f:
    data = json.load(f)

# Initialize an empty list to hold the quotes
quotes_list = []

# Remove >128
# my_list = [s for s in quotes_list if len(s) <= 128]

# Search for quotes in the data structure
find_quotes(data, quotes_list)

quotes_list = [filter_sent(q) for q in quotes_list]

clump = ' '.join(quotes_list)

print(clump)