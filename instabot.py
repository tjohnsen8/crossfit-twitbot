import CfInsta as cfi
import time


if __name__ == '__main__':
	insta = cfi.CfInstagram()
	while True:
		insta.repost()
		time.sleep(1000)