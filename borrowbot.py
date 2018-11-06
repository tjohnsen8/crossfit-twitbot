from CfReddit import CfReddit
from dataclasses import dataclass
from praw.models import MoreComments


@dataclass
class PostInfo:
	title: str
	text: str
	op: str
	loaned: bool

if __name__ == '__main__':
	rd = CfReddit()
	updates = rd.get_new_reddit_posts('borrow', 10)
	for update in updates:
		post = PostInfo(update.title, update.selftext, update.author, False)
		if '[REQ]' in post.title:
			for comment in update.comments.list():
				if '$loan' in comment.body:
					post.loaned = True
					break
			if post.loaned:
				continue
			# get the amount now
			s = post.title
			print(s[s.find("(")+1:s.find(")")])