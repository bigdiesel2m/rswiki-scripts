## Script for pulling newspost images from Steam's API

import requests
import json
import shutil
import os.path

## THIS SECTION HANDLES CREATING THE LIST OF HEADER IMAGES

API_URL = "https://api.steampowered.com/ISteamNews/GetNewsForApp/v2/"
def getimglist():
	params = {
		"appid": "1343370",
		"count": "500", #Note: as of Sept 3rd, 2024, there are 276 total newsposts
	}

	response = requests.get(API_URL, params=params)
	responsejson = response.json()

	newsitems = responsejson['appnews']['newsitems']

	imglist = {}
	for newspost in newsitems:
		contents = newspost['contents']
		title = newspost['title']
		if '[img]' in contents:
			firstimg = contents.split('[img]')[1].split('[/img]')[0]
		else:
			firstimg = ''
		if title in imglist:
			title = title + '-0'
		imglist[title] = firstimg

	with open('steam/imglist.json', 'w') as outfile:
		json.dump(imglist, outfile)
	return(imglist)

imglist = []
regenimglist = False
if regenimglist:
	imglist = getimglist()
else:
    with open('steam/imglist.json') as infile:
        imglist = json.load(infile)

## THIS SECTION HANDLES DOWNLOADING THE HEADER IMAGES

BASE_URL = 'https://clan.akamai.steamstatic.com/images/'
def donwloadimg(newsname,imgstring):
	fullurl = BASE_URL + imgstring[18:]
	cleanname = newsname.split('|')[0].strip().replace('/','-').replace(':','-')
	extension = imgstring.split('.')[1]
	filename = cleanname + " Steam newspost." + extension

	if not os.path.isfile('steam/images/' + filename):
		print(filename)
		response = requests.get(fullurl, stream = True)
		with open('steam/images/' + filename, 'wb') as outfile:
			shutil.copyfileobj(response.raw, outfile)
		del response

for img in imglist:
	if len(imglist[img]) > 0:
		donwloadimg(img,imglist[img])