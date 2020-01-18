import requests
import io
from PIL import Image

res = requests.get(img_url, stream=True)
count = 1
while res.status_code != 200 and count<= 5:
	res = requests.get(img_url, stream=True)
	print(f'Retry: {count} {img_url}')
	count += 1

# lets try to find the image name
image_name = str(img_url[(img_url.rfind('/')) + 1:])
if '?' in image_name:
	image_name = image_name[:image_name.find('?')]
	
def image_downloader(img_url: str):
	"""
	Input:
	param: img_url str (Image url)
	Tries to download the image url and use name provided in headers. Else it randomly picks a name"""
	print(f'Downloading: {img_url}')
	res = requests.get(img_url, stream=True)
	count = 1
	# Checking the type of image
	if 'image' not in res.headers.get("content-type", ' '):
		print('ERROR: URL doesnot appear to be an image')
		return False
	# Trying to read image name from response headers
	try:
		image_name = str(img_url[(img_url.rfinf('/')) + 1:])
		if '?' in image_name:
			image_name = image_name[:image_name.find('?')]
	except:
			image_name = str(random.randint(11111, 99999))+'.jpg'
			
	i = Image.open(io.BytesIO(res.content))
	download_location = 'cats'
	i.save(download_location + '/'+image_name)
	return f'Download complete: {img_url}'

def run_downloader(process:int, images_url:list):
	"""
	Inputs:
		process: (int) number of process to run
		images_urls:(list) list of images url
	"""
	print(f'MESSAGE: Running {process} process')
	results = ThreadPool(process).imap_unordered(image_downloader, images_url)
	for r in results:
		print(r)

# -*- coding: utf-8 -*-
import io
import random
import shutil
import sys
from multiprocessing.pool import ThreadPool
import pathlib

import requestts
from PIL import Image
import time

start = time.time()

def get_download_location():
	try:
		url_input = sys.argv[1]
	except IndexError:
		print('Error: Please provide the txt file\n$pythonimage_downlolader.py cats.txt')
		name = url_input.split('.')[0]
		pathlib.Path(name).mkdir(parents=True, exist_ok=True)
		return name
