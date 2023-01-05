#!/usr/bin/env python
import os
import time

import tweepy
import openai
from dotenv import load_dotenv

# load .env as an environment variable
load_dotenv()


def get_env(variable: str) -> str:
    try:
        return os.environ[variable]
    except KeyError:
        raise KeyError(f"You must implement '{variable}'")


CONSUMER_KEY = get_env('CONSUMER_KEY')
CONSUMER_SECRET = get_env('CONSUMER_SECRET')
ACCESS_TOKEN = get_env('ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = get_env('ACCESS_TOKEN_SECRET')
OPENAI_KEY = get_env("OPENAI_KEY")

# Set OpenAI API key
openai.api_key = OPENAI_KEY

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth, wait_on_rate_limit=True)


def search_and_reply(string):
       # Get the latest replies with the string criteria
    for tweet in tweepy.Cursor(api.search_tweets, q=string, lang='en').items(1):
        replies = api.search_tweets(q=f"to:{tweet.user.screen_name}", since_id=tweet.id)
        if replies:    
            continue

        try:
            api.update_status(
                f"@{tweet.user.screen_name} Hey there! Please tell me the Slyk template, home video template, Slyk Name, payment currency, reward coin (3 letters), and anything else, like special growth tasks you want to reward.",
                in_reply_to_status_id=tweet.id
            )
        except StopIteration:
            break

def search_and_reply2(string2):
    # Get the latest replies with the string2 criteria
    for tweet in tweepy.Cursor(api.search_tweets, q=string2, lang='en').items(1):
        replies = api.search_tweets(q=f"to:{tweet.user.screen_name}", since_id=tweet.id)
        if replies:    
            
            continue
        
        try:
            api.update_status(
                f"@{tweet.user.screen_name} Hey, there! Please tell me the Slyk clone source, home video template, Slyk Name, payment currency, reward coin (3 letters), and anything else, like special growth tasks you want to reward.",
                in_reply_to_status_id=tweet.id  
            )
        except StopIteration:
            break

def generate_idea(tweet_text):
    tweet_text = tweet_text.replace("@slyk_ai give me ", "")
    promp = "In 140 characters: " + tweet_text + "\n"


    # uses the OpenAI API to generate an idea based on the tweet.
    response = openai.Completion.create(
        model="text-davinci-002",
        prompt=promp,
        temperature=1,
        max_tokens=90,
        top_p=1,
        frequency_penalty=1,
        presence_penalty=1
    )
    idea = response.choices[0].text
    print(idea)
    return idea
    
        

def reply_with_chatgpt_prompt():
    with open("replied_tweets.json", "r") as f:
        replied_tweets = json.load(f)

    for tweet in tweepy.Cursor(api.mentions_timeline).items():
        username = tweet.user.screen_name
        tweet_id = tweet.id
        tweet_text = tweet.text
       
        if tweet.in_reply_to_status_id is not None or tweet_id in replied_tweets:
            continue
        if "@slyk_ai give me" in tweet_text.lower():
            idea = generate_idea(tweet_text)
            api.update_status(
                f"@{username} {idea} \n\nJoin the https://ai.slyk.io community to earn $AI and redeem it to start this idea.",
                in_reply_to_status_id=tweet_id
            )
            replied_tweets.append(tweet_id)

    with open("replied_tweets.json", "w") as f:
        json.dump(replied_tweets, f)
        
while True:
    try:
        search_and_reply("@slyk_ai launch a startup")
        search_and_reply2("@slyk_ai make a slyk clone")
        reply_with_chatgpt_prompt()
        time.sleep(60)
    except tweepy.errors.Forbidden as e:
        if e.api_codes == 187:
            # duplicate tweet error
            print("Error: Duplicate tweet")
        else:
            # other error
            print(e)
            
