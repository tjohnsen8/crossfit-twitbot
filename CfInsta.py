from InstagramAPI import InstagramAPI
from credentials import instagram_client_id, instagram_client_secret
from os import remove
import requests
import json
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from dataclasses import dataclass
from time import sleep


def get_largest_image(candidates):
	candidate = {}
	pixels = 0
	for cand in candidates:
		# pick the highest resolution one
		res = cand['height']*cand['width']
		if res > pixels:
			pixels = res
			candidate = cand

	return candidate


def get_caption(item):
	caption = ''
	if 'caption' in item.keys():
		if 'text' in item['caption'].keys():
			caption = item['caption']['text']
	return caption


def trim_caption(status):
		words = status.split(' ')
		hashtags = [word[word.find('#'):] for word in words if '#' in word]
		if len(status) > 280:
			# remove the hashtags from the status
			status = status[:status.find('#')]
			hashtag_str = ' '.join(hashtags)
			hashtag_str_len = 140 # leave half the status for the message
			while len(hashtag_str) > hashtag_str_len:
				del hashtags[-1]
				hashtag_str = ' '.join(hashtags)
			status = '{}... {}'.format(status[:len(hashtag_str) - 4], hashtag_str)
		print(len(status))
		print(status)


def caption_test():
	status = \
	'Congrats to our athlete of the month, VAL!!! She has dialed ' + \
	'in her nutrition and pushed herself every time she steps into the gym. ' + \
	'We are so proud of her progress and can’t wait to watch the transformation continue! ' + \
	'Best of luck this weekend at the @swampchallenge @hiddenkey33 ' + \
	'#crossfitchicks #crossfithsn #crossfitnutrition #fitnessgirl #healthystepsnutrition #guidedtestedproven'
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
	print(status)


@dataclass
class IgMedia:
	photo: str
	username: str
	caption: str
	full_name: str
	media_type: int


class CfInstagram:
	def __init__(self, view_debug=False):
		self.already_tweeted = []
		self.view_debug = view_debug
		self.get_already_tweeted()
		self.api = InstagramAPI(instagram_client_id, instagram_client_secret)
		self.api.login()


	def get_already_tweeted(self):
		try:
			with open('twig.txt', 'r') as file:
				lines = file.readlines()
				for line in lines:
					self.already_tweeted.append(line.rstrip('\n'))
		except:
			print('error in file handling')


	def add_already_tweeted_to_file(self, id):
		try:
			with open('twig.txt', 'a') as file:
				file.write('{}\n'.format(str(id)))
		except:
			print('error in file handling')


	def save_image_from_candidate(self, url):
		response = requests.get(url)
		filename = url.split("/")[-1].split('?')[0]
		if response.status_code == 200 and not filename in self.already_tweeted:
			with open(filename, 'wb') as f:
				f.write(response.content)
			self.add_already_tweeted_to_file(filename)
			self.already_tweeted.append(filename)
		else:
			filename = ''
		return filename
	

	def get_images_from_hashtag(self, hashtag, num_images):
		images = []
		'''
		list of 
		class IgMedia:
			photo: str
			username: str
			caption: str
			full_name: str
			media_type: int
		'''
		get_hashtag = self.api.getHashtagFeed(hashtag)

		if get_hashtag == False:
			return images

		for item in self.api.LastJson['items']:
			if item['media_type'] == 1 and 'image_versions2' in item.keys():
				candidate = get_largest_image(item['image_versions2']['candidates'])
				# get image 
				filename = self.save_image_from_candidate(candidate['url'])
				if filename != '':
					# get status, save as tuple
					caption = get_caption(item)
					#images.append((filename, caption))
					images.append(IgMedia(filename, item['user']['username'], caption, \
						item['user']['full_name'], item['media_type']))
				if len(images) >= num_images:
					break
				if self.view_debug:
					try:
						img = mpimg.imread(filename)
						imgplot = plt.imshow(img)
						plt.show()
					except OSError:
						print('not an image')
		return images


	def get_ig_updates(self):
		# get the hashtags from a file
		self.hashtags = []
		try:
			with open('ig_hashtags.txt') as file:
				lines = file.readlines()
				for line in lines:
					self.hashtags.append(line.rstrip('\n'))
		except:
			print('error handling hashtags file')

		updates = []
		for hashtag in self.hashtags:
			images = self.get_images_from_hashtag(hashtag, 1)
			updates.extend(images)
		return updates


	def repost(self):
		updates = self.get_ig_updates()
		for post in updates:
			self_caption = f"Coverage Breakdown Repost:\n\n\nvia {post.full_name} @{post.username} "
			self_caption += "\n\n\n"
			self_caption += post.caption
			print(self_caption)
			self.api.uploadPhoto(post.photo, self_caption)
			remove(post.photo)
			sleep(2)


	def upload_photo(self, photo_path, caption):
		self.api.uploadPhoto(photo_path, caption)


	def get_captions_test(self, hashtag):
		captions = []
		get_hashtag = self.api.getHashtagFeed(hashtag)

		if get_hashtag == False:
			return images

		for item in self.api.LastJson['items']:
			captions.append(get_caption(item))
		return captions


if __name__ == '__main__':
	#caption_test()
	ig = CfInstagram();
	#images = ig.get_images_from_hashtag('healthystepsnutrition', 5)
	#updates = ig.get_ig_updates()
	#print(updates)
	#ig.upload_photo('42496462_251259842409640_3534980390928554836_n.jpg', "Walking into the voter booth like .... \n\n\n #vote #whyivote #crossfit #handstandwalk")
	ig.repost()

	#captions = ig.get_captions_test('healthystepsnutrition')
	#for caption in captions:
	#	trim_caption(caption)
