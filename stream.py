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

    def on_status(self, source):
        try:
            author = source.author.screen_name
            text =  source.text
            tweet_id = source.id
            if ((author == 'realDonaldTrump') | ("@Trump_LSTM" in text)) & (author != 'Trump_LSTM'):
                mention = '@' + author + ' '
                tweet = generate_tweet(text, 0.6, prepend = mention)
                self.api.update_status(tweet, tweet_id)
        except: 
          pass
        return True

    def on_error(self, status):
        print status
        if status == 420:
            #returning False in on_data disconnects the stream
            return False


if __name__ == '__main__':

    #This handles Twitter authetification and the connection to Twitter Streaming API
    auth = OAuthHandler(keys["consumer_key"], keys["consumer_secret"])
    auth.set_access_token(keys["access_token"], keys["access_token_secret"])
    l = StdOutListener()
    l.set_auth(auth)
    stream = Stream(auth, l)
    stream2 = Stream(auth, l)

    stream.filter(follow=['25073877'], track=['Trump_LSTM'])



