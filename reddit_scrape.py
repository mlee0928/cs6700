import requests
import praw
import pandas as pd
import json

with open("access_vars.json", "r", encoding="utf-8") as f:
    d = json.load(f)

app_id = d["app_id"]
reddit_password = d["password"]
secret = d["secret"]
reddit_username = d["username"]

auth = requests.auth.HTTPBasicAuth(app_id, secret)

data = {
'grant_type': 'password',
'username': reddit_username,
'password': reddit_password
}
headers = {'User-Agent': 'gettoken'}

reddit = praw.Reddit(client_id=app_id,
                     client_secret=secret,
                     user_agent='gettoken',
                     username=reddit_username,
                     password=reddit_password)

print(reddit.read_only)
print(reddit.user.me())

res = requests.post('https://www.reddit.com/api/v1/access_token',
                    auth=auth, data=data, headers=headers)
print(res)
print(res.json())

token = res.json()['access_token']
headers['Authorization'] = 'bearer {}'.format(token)
requests.get('https://oauth.reddit.com/api/v1/me', headers=headers)

api = 'https://oauth.reddit.com'
res = requests.get('{}/r/ethtrader/new'.format(api), headers=headers, params={'limit': '100'})
res.json()

df = pd.DataFrame({'name': [], 'title': [], 'selftext': [], 'score': []})
for post in res.json()['data']['children']:
  df = df.append({
    'name': post['data']['name'],
    'title': post['data']['title'],
    'selftext': post['data']['selftext'],
    'score': post['data']['score']}, ignore_index=True)
print(df)

submission = reddit.submission("v1jln5")
for top_level_comment in submission.comments:
    print(top_level_comment.body)

hot_posts = reddit.subreddit('news').hot(limit=10)
"""
top_ten = {
    top_level_comment1: {
        second_level_comment1: {
            [
                third_level_comment1,
                third_level_comment2
            ]
        },
        second_level_comment2: {
            [
                third_level_comment3,
                third_level_comment4
            ]
        }
    },
    top_level_comment2: {
        ...
    }
}
"""
top_ten = {}
for post in hot_posts:
    print("post id:", post)
    submission = reddit.submission(post)
    # TODO: randomly extract 10 comments and get all subthreads until level 3
    submission.comments.replace_more()
    # submission.replace_more_comments(limit=None, threshold=0)
    post_id = str(post)
    top_ten[post_id] = {}
    for top_level_comment in submission.comments:
        top = str(top_level_comment.body)
        top_ten[post_id][top] = {}
        for second_level_comment in top_level_comment.replies:
            second = str(second_level_comment.body)
            top_ten[post_id][top][second] = []
            for third_level_comment in second_level_comment.replies:
                third = third_level_comment.body
                top_ten[post_id][top][second].append(third)
print(top_ten)
with open("top_ten.json", "w", encoding="utf-8") as f:
    json.dump(top_ten, f)
