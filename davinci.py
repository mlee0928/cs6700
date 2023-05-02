import os
import json

import openai
from flask import Flask, redirect, render_template, request, url_for

with open("key.txt", "r", encoding="utf-8") as f:
    key = f.readline().strip()
app = Flask(__name__)
openai.api_key = key


def openai_create(par):
    prompt = f'summarize the below text\n\n"{" ".join(par)}'
    response = openai.Completion.create(
        engine="text-davinci-003", prompt=prompt, temperature=0, max_tokens=100)
    return response


def get_summary(par):
    response = openai_create(par)
    return response["choices"][0]["text"]

with open("top_ten.json", "r", encoding="utf-8") as f:
    top_ten = json.load(f)


for top in top_ten:
    paragraph = top.strip()
    for second in top_ten[top]:
        paragraph += second.strip()
        for third in top_ten[top][second]:
            paragraph += third.strip()
    print("-----------------------------------------------------------")
    print(paragraph)