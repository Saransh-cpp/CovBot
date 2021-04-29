import tweepy
from tweepy import OAuthHandler
import time
from keys import Keys

access_token = Keys.ACCESS_KEY
access_token_secret = Keys.ACCESS_SECRET
consumer_key = Keys.CONSUMER_KEY
consumer_secret = Keys.CONSUMER_SECRET

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

for tweet in tweepy.Cursor(api.search, q='Covid').items(5):
    try:
        print('\nFound by @' + tweet.user.screen_name)

        tweet.retweet()
        print('Retweeted')

        time.sleep(10)

    except tweepy.TweepError as error:
        print(error.reason)

    except StopIteration:
        break