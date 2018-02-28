import tweepy
import time
from credentials import *

# Access and authorize our Twitter credentials from credentials.py
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

def get_update_time():
	# read the last time updated from a file
	return time.time()

if __name__ == '__main__':
	# For loop to iterate over tweets with #ocean, limit to 10
	update_time = get_update_time()
	for tweet in tweepy.Cursor(api.search,q='#crossfitopen').items(10):
	# Print out usernames of the last 10 people to use #ocean
		try:
			print('Tweet by: @' + tweet.user.screen_name)
			print(tweet.text)
			tweet.retweet()
			print('rewtweeted')
			time.sleep(1)
		except tweepy.TweepError as e:
			print(e.reason)
		except StopIteration:
			break

'''
	    ['__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', 
	    '__format__', '__ge__', '__getattribute__', '__getstate__', '__gt__', '__hash__',
	    '__init__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', 
	    '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__',
	    '__weakref__', '_api', '_json', 'author', 'contributors', 'coordinates', 'created_at',
	    'destroy', 'entities', 'favorite', 'favorite_count', 'favorited', 'geo', 'id', 
	    'id_str', 'in_reply_to_screen_name', 'in_reply_to_status_id', 'in_reply_to_status_id_str', 
	    'in_reply_to_user_id', 'in_reply_to_user_id_str', 'is_quote_status', 'lang', 'metadata', 
	    'parse', 'parse_list', 'place', 'possibly_sensitive', 'retweet', 'retweet_count', 
	    'retweeted', 'retweets', 'source', 'source_url', 'text', 'truncated', 'user']
'''
