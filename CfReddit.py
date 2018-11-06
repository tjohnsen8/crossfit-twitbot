import praw
from credentials import *

class CfReddit:
	def __init__(self):
		self.reddit = praw.Reddit(client_id=reddit_client_id,
			client_secret=reddit_client_secret,
			user_agent=reddit_user_agent)
		self.already_tweeted = []
		self.get_already_tweeted()


	def get_subs_for_tweets(self):
		self.subs = []
		try:
			with open('subreddits.txt') as file:
				lines = file.readlines()
				for line in lines:
					self.subs.append(line.rstrip('\n'))
		except:
			print('error handling subs file')


	def get_already_tweeted(self):
		try:
			with open('twrd.txt', 'r') as file:
				lines = file.readlines()
				for line in lines:
					self.already_tweeted.append(line.rstrip('\n'))
		except:
			print('error in file handling')


	def add_already_tweeted_to_file(self, id):
		try:
			with open('twrd.txt', 'a') as file:
				file.write('{}\n'.format(str(id)))
		except:
			print('error in file handling')


	def get_reddit_updates(self, num_posts=10):
		updates = []
		self.get_subs_for_tweets()
		for sub in self.subs:
			for submission in self.reddit.subreddit(sub).new(limit=num_posts):
				title = submission.title
				url = 'www.reddit.com{}'.format(submission.permalink)
				if not submission in self.already_tweeted:
					tweet_str = 'Reddit r/{} update:\n\n{} #{} {}'.format(sub, title, sub, url)
					updates.append(tweet_str)
					self.already_tweeted.append(submission)
					self.add_already_tweeted_to_file(submission)
				else:
					print('already tweeted {}'.format(submission))
		return updates

	def get_new_reddit_posts(self, sub_name, max_posts=30):
		posts = []
		for submission in self.reddit.subreddit(sub_name).new(limit=max_posts):
			posts.append(submission)
		return posts