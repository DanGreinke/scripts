#!/usr/bin/env python3.8

import tweepy
import yaml


#Import YAML Data
with open("../secrets.yaml", "r") as f:
    AUTH_DICT = yaml.load(f, Loader=yaml.FullLoader)


#Authenticate to Twitter
AUTH = tweepy.OAuthHandler(AUTH_DICT['TWITTER_API'], AUTH_DICT['TWITTER_API_SECRET'])
AUTH.set_access_token(AUTH_DICT['TWITTER_ACCESS_TOKEN'], AUTH_DICT['TWITTER_ACCESS_TOKEN_SECRET'])

API = tweepy.API(AUTH)

try:
    API.verify_credentials()
    print("Authentication OK")
except:
    print("Error during authentication")


#Post a tweet
API.update_status("Hello world")
