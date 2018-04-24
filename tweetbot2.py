import CfTwitter as cft
import CfReddit as cfr
import CfInsta as cfi
import time


if __name__ == '__main__':
	tw = cft.CfTwitter()
	rd = cfr.CfReddit()
	ig = cfi.CfInstagram()
	while True:
		tw.do_retweets(5)
		statuses = rd.get_reddit_updates()
		tw.do_tweets(statuses)
		ig_media = ig.get_ig_updates()
		tw.do_media_tweets(ig_media)
		time.sleep(1000)