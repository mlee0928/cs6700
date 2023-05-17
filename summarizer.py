import openai
import re
import json

with open("openai_key.txt") as f:
    key = f.readline().strip()

openai.api_key = key


def generatePrompt(summary):
    return f"{summary}\\n\\nTl;dr"

def generateSentimentPrompt(text, sent):
    prompt = f"These are quotes from various people about an article. {text}." \ 
             f"All of these comments have {sent} sentiment, please summarize what " \ 
             f"these people think about the article."
    return prompt

def generateSummaryPrompt(text):
    prompt = f"This a combination of people commenting on a thread. {text}." \
             f"Please summarize what " \
             f"these people are discussing."
    return prompt

def generateDetailsPrompt(text):
    prompt = f"This a combination of people commenting on a thread. {text}." \
             f"Please give me some specific details on what " \
             f"these people are discussing."
    return prompt

def summarizer(prompt, temp=0.7):
    response = openai.Completion.create(
        # TODO: change to gpt-4
        # TODO: try different temperature (0 is conservative, 1 is creative)
        model="text-davinci-003",
        prompt=prompt,
        temperature=temp,
        max_tokens=200,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=1
    )

    result = response["choices"][0]["text"]
    # print(result)
    result = re.sub('^[^a-zA-Z0-9\.\)]*|[^a-zA-Z0-9\.\)]*$', '', result)

    return result

def sentiment_summ(prompt, sent, temp=0.7):
    response = openai.Completion.create(
        # TODO: change to gpt-4
        # TODO: try different temperature (0 is conservative, 1 is creative)
        model="text-davinci-003",
        prompt=generateSentimentPrompt(prompt, sent),
        temperature=temp,
        max_tokens=200,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=1
    )

    result = response["choices"][0]["text"]
    # print(result)
    result = re.sub('^[^a-zA-Z0-9\.\)]*|[^a-zA-Z0-9\.\)]*$', '', result)

    return result

with open('clump.json', 'r') as f:
    clum_dict = json.load(f)

for thread_id in clum_dict:
    print(f"Thread_id: {thread_id}\n\
    Summary:\n {summarizer(generateSummaryPrompt(clum_dict[thread_id]))}\n \
    Details:\n {summarizer(generateDetailsPrompt(clum_dict[thread_id]))}\n\n")