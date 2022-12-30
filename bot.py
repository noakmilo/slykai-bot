#!/usr/bin/env python
import tweepy
#from our keys module (keys.py), import the keys dictionary
from keys import keys
import time

CONSUMER_KEY = keys['consumer_key']
CONSUMER_SECRET = keys['consumer_secret']
ACCESS_TOKEN = keys['access_token']
ACCESS_TOKEN_SECRET = keys['access_token_secret']

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth, wait_on_rate_limit=True)


def search_and_reply(string):
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
                        
while True:
    try:
        search_and_reply("@slyk_ai launch a startup")
        search_and_reply2("@slyk_ai make a slyk clone")
        time.sleep(30)
    except tweepy.errors.Forbidden as e:
        if e.api_codes == 187:
            # duplicate tweet error
            print("Error: Duplicate tweet")
        else:
            # other error
            print(e)
            
