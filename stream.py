#Import the necessary methods from tweepy library
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy import API
import json
from make_tweet import generate_tweet


#Variables that contains the user credentials to access Twitter API 
with open('secrets.json', 'r') as f:
    keys = json.loads(f.read())

#This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):
    def set_auth(self, auth):
        self.api = API(auth)

    def on_data(self, data):
        source = json.loads(data)
        mention = '@' + source['user']['screen_name'] + ' '
        tweet = generate_tweet(source['text'], 0.6)[:140 - len(mention)]
        response = mention + tweet
        self.api.update_status(response, source['id'])
        return True

    def on_error(self, status):
        print status


if __name__ == '__main__':

    #This handles Twitter authetification and the connection to Twitter Streaming API
    auth = OAuthHandler(keys["consumer_key"], keys["consumer_secret"])
    auth.set_access_token(keys["access_token"], keys["access_token_secret"])
    l = StdOutListener()
    l.set_auth(auth)
    stream = Stream(auth, l)

    #This line filter Twitter Streams to capture data by the keywords: 'python', 'javascript', 'ruby'
    stream.filter(track=['Trump_LSTM'])




