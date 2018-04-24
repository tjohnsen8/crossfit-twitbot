import tweepy
import time
from os import remove
from credentials import *


class CfTwitter:
	def __init__(self):
		# Access and authorize our Twitter & Reddit credentials from credentials.py
		self.auth = tweepy.OAuthHandler(twitter_consumer_key, twitter_consumer_secret)
		self.auth.set_access_token(twitter_access_token, twitter_access_token_secret)
		self.api = tweepy.API(self.auth)
		self.get_hashtags_for_rt()

	def trim_to_280(self, status):
		if len(status) > 200:
			status = status[:200]
		return status

	def trim_to_280_keep_hashtags(self, status):
		if len(status) > 280:
			# remove the hashtags from the status
			hashtags = [word[word.find('#'):] for word in status.split(' ') if '#' in word]
			status = status[:status.find('#')]
			hashtag_str = ' '.join(hashtags)
			hashtag_str_len = 140 # leave half the status for the message
			while len(hashtag_str) > hashtag_str_len:
				del hashtags[-1]
				hashtag_str = ' '.join(hashtags)
			status = '{}... {}'.format(status[:len(hashtag_str) - 4], hashtag_str)
		return status

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

	def do_retweets(self, num_retweets=20):
		self.get_hashtags_for_rt()
		for hashtag in self.hashtags:
			self.do_retweet(hashtag, num_retweets)

	def do_retweet(self, query_str, num_retweets):
		for tweet in tweepy.Cursor(self.api.search,q=query_str).items(num_retweets):
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
				status = self.trim_to_280(status)
				self.api.update_status(status)
				print(status)
				time.sleep(1)
			except tweepy.TweepError as e:
				print(e.reason)
			except StopIteration:
				break

	def do_media_tweets(self, media_tuples):
		for (filename, message) in media_tuples:
			try:
				message = self.trim_to_280_keep_hashtags(message)
				self.api.update_with_media(filename, status=message)
				print(message)
				remove(filename)
			except tweepy.TweepError as e:
				print(e.reason)
			except StopIteration:
				break


