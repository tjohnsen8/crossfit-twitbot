from InstagramAPI import InstagramAPI
from credentials import instagram_client_id, instagram_client_secret
import requests
import json
import matplotlib.pyplot as plt
import matplotlib.image as mpimg


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


def save_image_from_candidate(url):
	response = requests.get(url)
	filename = url.split("/")[-1].split('?')[0]
	if response.status_code == 200:
		with open(filename, 'wb') as f:
			f.write(response.content)
	else:
		filename = ''
	return filename


def get_images_from_hashtag(hashtag, num_images, view_debug=False):
	images = []
	api = InstagramAPI(instagram_client_id, instagram_client_secret)
	api.login()
	get_hashtag = api.getHashtagFeed(hashtag)

	if get_hashtag == False:
		return images
	
#	json_data = json.loads(api.LastJson)
	for item in api.LastJson['items']:
		if 'image_versions2' in item.keys():
			candidate = get_largest_image(item['image_versions2']['candidates'])
			# get image 
			filename = save_image_from_candidate(candidate['url'])
			if filename != '':
				# get status, save as tuple
				caption = get_caption(item)
				images.append((filename, caption))
			if len(images) > num_images:
				break
			if view_debug:
				try:
					img = mpimg.imread(filename)
					imgplot = plt.imshow(img)
					plt.show()
				except OSError:
					print('not an image')
	return images

if __name__ == '__main__':
	images = get_images_from_hashtag('healthystepsnutrition', 10, False)
	print(images)