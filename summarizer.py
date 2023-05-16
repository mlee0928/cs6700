import openai
import re

with open("openai_key.txt") as f:
    key = f.readline().strip()

openai.api_key = key


def generatePrompt(summary):
    return f"{summary}\\n\\nTl;dr"


sample_text = "I remember reading about a minimum security prison escape in Colorado years ago. Dude was " \
              "Mexican and he left detailed maps all over his cell with the route he was going to take to " \
              "Canada. Yea, they had road blocks all they way to Canada and never found him."

def summarizer(text):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=generatePrompt(text),
        temperature=0.7,
        max_tokens=60,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=1
    )

    result = response["choices"][0]["text"]
    # print(result)
    result = re.sub('^[^a-zA-Z0-9\.\)]*|[^a-zA-Z0-9\.\)]*$', '', result)

    return result

print(summarizer(sample_text))