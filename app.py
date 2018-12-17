"""<=== import module and package ===>"""
import tweepy
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import re
import pandas as pd
import webbrowser
import time
from time import gmtime, strftime

"""<=== Input Hashtags ===>"""
Your_hashtags = input("Enter your Hashtags ==> ")

"""<=== Open index.html in webbrowser ===>"""
time.sleep(1)
webbrowser.open("templates\index.html")

"""<=== Api Key ===>"""
consumer_key = "3II162EiHwgcNCSV17YW0Ykof"
consumer_secret = "CZonbTz3tao9tZkQVVCvQscf5Yml0ohV3H2n16JYktg4bY73z4"
access_token = "1349083645-NoM2NjgwsSqPPrT3DN8PgKMa4VFV8VGpV7qVX1H"
access_token_secret = "wI0pzHELnIIMzTZPLm4Pn7Gj01SVL5zniJaDPM2ZcW6SG"
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

"""<=== Dictionary to get Hashtags ===>"""
dict_hashtags = {}

"""<=== Stream data ===>"""
class MyListener(StreamListener):
    def on_data(self, data):
        try:
            
            """<=== Cleaning Data ===>"""
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
            
            """<=== Get Hashtags to Dictionary ===>"""
            hashtags = [hashtag.lower() for hashtag in tokenize(data) if len(hashtag)>1 and hashtag[0]=="#"]
            for i in hashtags:
                if i not in dict_hashtags:
                    dict_hashtags[i] = [i, 1]
                else:
                    dict_hashtags[i][1] += 1

            """<=== Create Dataframe and Get the most Hashtags ===>"""
            df_hashtags =  pd.DataFrame.from_dict(dict_hashtags, orient='index', columns=['hash', 'count'])
            df_hashtags = df_hashtags.sort_values(by='count', ascending=False)
            results = df_hashtags.head(5)
            df = results.values.tolist()

            """<=== Delete # ===>"""
            dict_json = {}
            for i in df:
                i[0] = i[0].lstrip("#")
                dict_json[i[0]] = i[1]
            dict_json = str(dict_json)
            dict_json = dict_json.replace("'", '"')

            """<=== Write the most Hashtags to .txt file ===>"""
            with open('Hashtags.txt', 'w', encoding='utf8') as f:
                f.write(str(dict_json))
                f.close()
            time.sleep(1)
            print(data)
        except BaseException as e:
            """<=== When data error ===>"""
            print("Error on_data: %s" % str(e))
        return True
    def on_error(self, status):
        """<=== When api error ===>"""
        print(status)


if __name__ == "__main__":
    stream = Stream(auth, MyListener())
    stream.filter(track=[Your_hashtags])
            
