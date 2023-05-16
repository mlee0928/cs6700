import openai
import re

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


sample_text = "I remember reading about a minimum security prison escape in Colorado years ago. Dude was " \
              "Mexican and he left detailed maps all over his cell with the route he was going to take to " \
              "Canada. Yea, they had road blocks all they way to Canada and never found him."

def summarizer(prompt, temp=0.7):
    response = openai.Completion.create(
        # TODO: change to gpt-4
        # TODO: try different temperature (0 is conservative, 1 is creative)
        model="text-davinci-003",
        prompt=generatePrompt(prompt),
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

# print(summarizer(sample_text))