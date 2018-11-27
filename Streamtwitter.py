import tweepy
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import csv
import re

consumer_key = "3II162EiHwgcNCSV17YW0Ykof"
consumer_secret = "CZonbTz3tao9tZkQVVCvQscf5Yml0ohV3H2n16JYktg4bY73z4"
access_token = "1349083645-NoM2NjgwsSqPPrT3DN8PgKMa4VFV8VGpV7qVX1H"
access_token_secret = "wI0pzHELnIIMzTZPLm4Pn7Gj01SVL5zniJaDPM2ZcW6SG"

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

class MyListener(StreamListener):
    def on_data(self, data):
        print(data)
        hashtags = [hashtag.lower() for hashtag in re.split('\s+', data) if len(hashtag)>0 and hashtag[0]=="#"]
        hashtags_clean = 
        with open('python.csv', 'a', encoding='utf8') as f:
            f.write(str(hashtags))
            f.write("\n")
    def on_error(self, status):
        print(status)

if __name__ == "__main__":
    stream = Stream(auth, MyListener())
    stream.filter(track=["#bnk48"])
            
