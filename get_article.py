import json
from summarizer import *
import re
from sentiment import filter_sent
import random

with open('top_ten.json', 'r') as f:
    top_ten = json.load(f)

with open('quote_sentiment.json', 'r') as f:
    quote_sentiment = json.load(f)

random.seed(42)
def get_sentiment_paragraph(thread_id):
    # TODO: fix sentence grabbing from top_ten
    all_quotes = {'POS': [], 'NEG': [], 'NEU': []}
    results = {}
    d = top_ten[thread_id]
    for top in d:
        label, score = quote_sentiment[filter_sent(top)]
        all_quotes[label].append(filter_sent(top))
        for second in d[top]:
            if second in quote_sentiment:
                label, score = quote_sentiment[filter_sent(second)]
                all_quotes[label].append(filter_sent(second))
            for third in d[top][second]:
                if third in quote_sentiment:
                    label, score = quote_sentiment[filter_sent(third)]
                    all_quotes[label].append(filter_sent(third))

    for quote_sent in all_quotes:
        lst = all_quotes[quote_sent]
        random.shuffle(lst)
        # print(lst)
        text = ""
        for item in lst:
            if len(text) + len(item) < 4090:
                text += ", "
                text += item

        # text = ",".join(lst)
        if quote_sent == 'POS':
            sent = 'positive'
        elif quote_sent == 'NEG':
            sent = 'negative'
        else:
            sent = 'neutral'
        print(sent)
        # print(text)
        result = sentiment_summ(text, sent)
        print(result)
        results[sent] = result

        # print(result)
    return results['positive'], results['negative'], results['neutral']


# for thread_id in top_ten:
#     get_sentiment_paragraph(thread_id)
thread_id = "133u8nd"
pos, neg, neu = get_sentiment_paragraph(thread_id)
