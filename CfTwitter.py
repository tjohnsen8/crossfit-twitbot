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
		for tweet in tweepy.Cursor(self.api.search,q=query_str).items(20):
			try:
				if tweet.user.screen_name.lower() == 'crossfit' or tweet.user.screen_name.lower() == 'crossfitgames':
					tweet.favorite()
					tweet.retweet()
				elif tweet.user.screen_name.lower() == 'sergbbk4' or tweet.user.screen_name.lower() == 'crossfittrump':
					pass
				else:
					tweet.retweet()
				
				print('Tweet by: @' + tweet.user.screen_name)
				print(tweet.text)
				print('\n\n')
				time.sleep(2)
			except tweepy.TweepError as e:
				print(e.reason)
			except StopIteration:
				break


	def do_tweets(self, status_list):
		for status in status_list:
			try:
				self.api.update_status(status)
				print(status)
				time.sleep(1)
			except tweepy.TweepError as e:
				print(e.reason)
			except StopIteration:
				break

