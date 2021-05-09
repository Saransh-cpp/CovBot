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

api = tweepy.API(
    auth, 
    # wait_on_rate_limit=True, 
    # wait_on_rate_limit_notify=True
    )

FILE_NAME = "lastSeenId.txt"

keywords = [
    "hospital",
    "bed",
    "oxygen",
    "icu",
    "cylinder",
    "urgent",
    "required",
    "available",
    "ventilator",
    "langar",
    "remdesivir",
    "plasma",
    "o+",
    "a+",
    "b+",
    "ab+",
    "o-",
    "a-",
    "b-",
    "ab-",
    "blood",
    "donate",
    "covidsos",
    "concentrator"
]


def retrieve_last_seen_id(file_name):
    f_read = open(file_name, "r")
    last_seen_id = int(f_read.read().strip())
    f_read.close()
    return last_seen_id


def store_last_seen_id(last_seen_id, file_name):
    f_write = open(file_name, "w")
    f_write.write(str(last_seen_id))
    f_write.close()
    return


def reply_to_tweet():
    print("replying...")
    last_seen_id = retrieve_last_seen_id(FILE_NAME)

    mention = api.mentions_timeline(last_seen_id, tweet_mode="extended")

    for singleMention in reversed(mention):
        print(
            str(singleMention.id) + " - " + singleMention.full_text
        )  # printing all my tweets
        last_seen_id = singleMention.id
        store_last_seen_id(last_seen_id, FILE_NAME)
#         singleMention.retweet()


reply_to_tweet()

for tweet in tweepy.Cursor(api.search, q="covid -filter:retweets", lang='en').items(50000):
    tweet_text = tweet._json['text']
    found = True
    try:
        for keyword in keywords:
            if found:
                if keyword in tweet_text.lower():
                    found = False
                    print("\nFound by @" + tweet.user.screen_name + " " + tweet_text)

                    # tweet.retweet()
                    print("Retweeted")

                    time.sleep(300)

    except tweepy.TweepError as error:
        print(error.reason)
