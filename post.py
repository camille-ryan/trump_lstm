#!/usr/bin/env python
# -*- coding: utf-8 -*-

#Import the necessary methods from tweepy library
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy import API
import json
from make_tweet import generate_tweet
import time
from random import randint

#Variables that contains the user credentials to access Twitter API 
with open('secrets.json', 'r') as f:
    keys = json.loads(f.read())


if __name__ == '__main__':

    #This handles Twitter authetification and the connection to Twitter Streaming API
    auth = OAuthHandler(keys["consumer_key"], keys["consumer_secret"])
    auth.set_access_token(keys["access_token"], keys["access_token_secret"])
    api = API(auth)

    #time.sleep(randint(0,5400))
    tweet = generate_tweet(u'#MAGA!', 0.6)
    for i in range(randint(2,5)):
        tweet = generate_tweet(tweet + u'', 0.4)
        api.update_status(tweet)
        time.sleep(randint(10,300))

