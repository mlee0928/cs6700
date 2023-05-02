from transformers import pipeline

models = ["textattack/roberta-base-imdb", "textattack/roberta-base-rotten-tomatoes",
          "finiteautomata/bertweet-base-sentiment-analysis"]
sentiment_analysis = pipeline("sentiment-analysis", model=models[2])

samples = [
    "Dude took off to Mexico. He's long gone by now.",
 "Yes, my first thought is execution style murders and the Hispanic perpetrator "
 "in Texas has now disappeared... bro jumped the border and disappeared into Mexico.",
 "Some Lalo Salamanca type shit",
 "it seems like he owns the house tho, why would he abandon his house?",
 "I remember reading about a minimum security prison escape in Colorado years ago. "
 "Dude was Mexican and he left detailed maps all over his cell with the route "
 "he was going to take to Canada. Yea, they had road blocks all they way to "
 "Canada and never found him.",
 "Would be pretty funny if that was all false leads. He actually went south. "
 "Would make sense. I'd bet that was the plan.",
 "My first thought, really no where else to go",
 "Thought same thing they said he's Hispanic.",
 "And yall call Texans racists lmao.",
"i love bubbles",
    "today is a lovely day, I am excited to go to class, i'm very happy",
"i am going to class"]
for text in samples:
    result = sentiment_analysis(text)[0]
    print(text)
    print(f"Sentiment: {result['label']}, Score: {result['score']}\n")