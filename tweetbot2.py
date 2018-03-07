import CfTwitter as cft
import CfReddit as cfr
import time


if __name__ == '__main__':

	# test writing to file
	tw = cft.CfTwitter()
	rd = cfr.CfReddit()
	while True:
		tw.do_retweets()
		statuses = rd.get_reddit_updates()
		tw.do_tweets(statuses)
		time.sleep(1000)