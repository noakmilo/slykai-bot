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


def search_and_reply(query):
    """
    Get the latest replies with the string criteria
    """
    for tweet in tweepy.Cursor(api.search_tweets, q=query, lang='en').items(1):
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


def reply_with_chatgpt_prompt(user_request):
    model_engine = "text-davinci-002"
    completion = openai.Completion.create(engine=model_engine, prompt=user_request, max_tokens=120, n=1,stop=None,temperature=1)
    response = completion.choices[0].text
   
    # Get the latest replies with the user_request criteria

    for tweet in tweepy.Cursor(api.search_tweets, q=user_request, lang='en').items(1):
        replies = api.search_tweets(q=f"to:{tweet.user.screen_name}", since_id=tweet.id)
        if replies:  
              
            continue
        
        try:
            api.update_status(
                f"@{tweet.user.screen_name} Here is your #StartupIdea generated with #ChatGPT👇 \n\n {response} \n\nJoin the https://ai.slyk.io community to earn $AI and launch this idea with Slyk.",
                in_reply_to_status_id=tweet.id
            )     
        except StopIteration:
            break
                        


if __name__ == "__main__":
    while True:
        try:
            search_and_reply("@slyk_ai launch a startup")
            search_and_reply2("@slyk_ai make a slyk clone")
            reply_with_chatgpt_prompt("@slyk_ai give me a startup idea")
            time.sleep(800)
        except tweepy.errors.Forbidden as e:
            if e.api_codes == 187:
                # duplicate tweet error
                print("Error: Duplicate tweet")
            else:
                # other error
                print(e)

