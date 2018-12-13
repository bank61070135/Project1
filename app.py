import tweepy
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import re
import pandas as pd
import matplotlib.pyplot as plt
from IPython import display
import time
from datetime import datetime, timedelta
from matplotlib.ticker import MaxNLocator
import matplotlib.animation as animation

consumer_key = "3II162EiHwgcNCSV17YW0Ykof"
consumer_secret = "CZonbTz3tao9tZkQVVCvQscf5Yml0ohV3H2n16JYktg4bY73z4"
access_token = "1349083645-NoM2NjgwsSqPPrT3DN8PgKMa4VFV8VGpV7qVX1H"
access_token_secret = "wI0pzHELnIIMzTZPLm4Pn7Gj01SVL5zniJaDPM2ZcW6SG"


auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

dict_hashtags = {}

class MyListener(StreamListener):
    def on_data(self, data):
        try:
            start_time = datetime.now()
            stream_period = 60
            finish_time = start_time + timedelta(minutes=stream_period)
            while datetime.now() < finish_time:
                wait_time = 10
                time.sleep(wait_time)
                stream_time = datetime.now()
                print(data)
                regex_str = [
                    r'<[^>]+>',
                    r'(?:@[\w_]+)',
                    r"(?:\#+[\w_]+[\w\'_\-]*[\w_]+)",
                    r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&amp;+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+',
                    r'(?:(?:\d+,?)+(?:\.?\d+)?)',
                    r"(?:[a-z][a-z'\-_]+[a-z])",
                    r'(?:[\w_]+)',
                    r'(?:\S)'
                    ]
                tokens_re = re.compile(r'('+'|'.join(regex_str)+')', re.VERBOSE | re.IGNORECASE)
                def tokenize(s):
                    return tokens_re.findall(s)
                hashtags = [hashtag.lower() for hashtag in tokenize(data) if len(hashtag)>1 and hashtag[0]=="#"]
                for i in hashtags:
                    if i not in dict_hashtags:
                        dict_hashtags[i] = [1]
                    else:
                        dict_hashtags[i][0] += 1

                df_hashtags =  pd.DataFrame.from_dict(dict_hashtags, orient='index', columns=['count'])
                df_hashtags = df_hashtags.sort_values(by='count', ascending=False)
                #results = df_hashtags.head(5)
                print(df_hashtags)
                with open('Hashtags.txt', 'w', encoding='utf8') as f:
                    f.write(str(df_hashtags))
                    f.close()
                """fig, ax = plt.subplots(1,1,figsize=(12,6))
                results.plot(kind='bar', x='hashtag', y='count', legend=False, ax=ax)
                ax.set_title("Top 5 hashtags")
                ax.set_xlabel("Hashtag", fontsize=18)
                ax.set_ylabel("Count", fontsize=18)
                ax.set_xticklabels(ax.get_xticklabels(), {"fontsize":14}, rotation=30)
                ax.yaxis.set_major_locator(MaxNLocator(integer=True))
                plt.yticks(fontsize=14)
                display.clear_output(wait=True)
                print("start time:", start_time.strftime('%Y-%m-%d %H:%M:%S'))
                print("stream time:", stream_time.strftime('%Y-%m-%d %H:%M:%S'))
                plt.show()"""
        except BaseException as e:
            print("Error on_data: %s" % str(e))
        return True
    def on_error(self, status):
        print(status)


if __name__ == "__main__":
    stream = Stream(auth, MyListener())
    stream.filter(track=["#bnk48"])
            
