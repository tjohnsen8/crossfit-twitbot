import tweepy
import time
from credentials import *


class CfTwitter:
	def __init__(self):
		# Access and authorize our Twitter & Reddit credentials from credentials.py
		self.auth = tweepy.OAuthHandler(twitter_consumer_key, twitter_consumer_secret)
		self.auth.set_access_token(twitter_access_token, twitter_access_token_secret)
		self.api = tweepy.API(self.auth)
		self.get_hashtags_for_rt()

	def get_hashtags_for_rt(self):
		self.hashtags = []
		try:
			with open('hashtags.txt') as file:
				lines = file.readlines()
				for line in lines:
					self.hashtags.append(line.rstrip('\n'))
		except:
			print('error handling hashtags file')

	def get_statuses_from_users(self):
		self.crossfit_tweets = []

	def do_retweets(self):
		self.get_hashtags_for_rt()
		for hashtag in self.hashtags:
			self.do_retweet(hashtag)

	def do_retweet(self, query_str):
		for tweet in tweepy.Cursor(self.api.search,q=query_str).items(10):
		# Print out usernames of the last 10 people to use #ocean
			try:
				if tweet.user.screen_name == 'crossfit' or tweet.user.screen_name == 'crossfitgames':
					tweet.favorite()
					url = 'https://twitter.com/{}/status/{}'.format(tweet.user.screen_name, tweet.id)
					tweet_str = 'CrossFit Update {}'.format(url)
					self.api.update_status(tweet_str)
				else:
					tweet.retweet()
				
				print('Tweet by: @' + tweet.user.screen_name)
				print(tweet.text)
				print('\n\n')
			except tweepy.TweepError as e:
				print(e.reason)
			except StopIteration:
				break


	def do_tweets(self, status_list):
		for status in status_list:
			try:
				self.api.update_status(status)
				print(status)
			except tweepy.TweepError as e:
				print(e.reason)
			except StopIteration:
				break

