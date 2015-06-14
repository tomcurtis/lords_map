# -*- coding: utf-8 -*-
#make list of all lords with all info 

import json
import math
import requests
from bs4 import BeautifulSoup
import sys
import random

#load in existing data
lords_file = open("all-lords.json", "r")
lords = json.load(lords_file)
lords_file.close()

#deal with them in alphabetical order
lords.sort(key=lambda x: x['full_name'])

#unwanted fields to remove to save space
unwanted_fields = [
	'left_reason',
	'left_house',
	'house',
	'last_update',
	'entered_reason',
	'entered_house',
	'image',
	'image_width',
	'image_height'
]

#check voting descriptions look good
replace_list = {
	'mps': "MPs",
	"house of lords": "House of Lords",
	"trident": "Trident",
	"house of commons": "House of Commons",
	"england": "England",
	"english": "English",
	"scotland": "Scotland",
	"scottish": "Scottish",
	"wales": "Wales",
	"welsh": "Welsh",
	"ireland": "Ireland",
	"irish": "Irish",
	"britain": "Britain",
	"british": "British",
	"great britain": "Great Britain",
	'great british': "Great British",
	"iraq": "Iraq",
	" eu ": " EU ",
	"the eu": "the EU",
	"uk's": "UK's",
	" uk ": " UK ",
	"id cards": "ID cards",
}

#how strongly worded each view is
strengths = {
	"very strongly for": 3,
	"strongly for": 2,
	"moderately for": 1,
	"a mixture of for and against": 0,
	"never voted": 0,
	"moderately against": -1,
	"strongly against": -2,
	"very strongly against": -3
}

#map value from left range to right domain
def translate(value, leftMin, leftMax, rightMin, rightMax):
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin

    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)

    # Convert the 0-1 range into a value in the right range.
    return rightMin + (valueScaled * rightSpan)

#retrieve a document at a given URL as parsed html tree
def get_doc(source_url):
	response = requests.get(source_url)
	html = response.content
	doc = BeautifulSoup(html)
	return doc

#constants to help with processing map
min_lat = 50.09701
max_lat = 59.868355
min_lon = -7.443237
max_lon = 1.6613556
map_width = 700
map_height = 750
radius = 5

#make grid of all possible squares- check for empty ones
map_grid = {}
grid_width = map_width / radius
grid_height = map_height / radius

#load in attendance/rebellion rate
lords_xml_file = open("mp-info.xml", "r")
lords_xml = BeautifulSoup(lords_xml_file)
lords_xml_file.close()

#sort out our lords
lords_count = str(len(lords))
for lord in lords:
	lord_index = str(lords.index(lord) + 1)
	sys.stderr.write(lord_index + "/" + lords_count + "\n")

	#remove unwanted fields
	for field in unwanted_fields:
		if (field in lord):
			del lord[field]

	# #capitalise the full name
	lord['full_name'] = lord['full_name'].capitalize()
	lord['constituency'] = lord['constituency'].replace("\n", "")

	#work out where it fits on the map grid - exact value
	lat_map = translate(lord['lat'], max_lat, min_lat, 0, map_height)
	lon_map = translate(lord['lon'], min_lon, max_lon, 0, map_width)

	#snap to grid
	lat_map = math.floor(lat_map / radius) * radius;
	lon_map = math.floor(lon_map / radius) * radius;

	#make grid key (r-c) and see if it's in the grid yet
	grid_col = int(lon_map / radius)
	grid_row = int(lat_map / radius)
	grid_key = str(grid_row) + "-" + str(grid_col)

	#not in the grid already - nab the spot
	if (grid_key not in map_grid):
		lord['x'] = grid_col
		lord['y'] = grid_row
		map_grid[grid_key] = True

	#not there- have to do a random walk to find options
	else:
		available = [] #make list of all possibilities
		for r in xrange(0, grid_height):
			for c in xrange(0, grid_width):
				poss_key = str(r) + "-" + str(c)
				if (poss_key not in map_grid):
					possibility = {
						'row': r,
						'col': c,
						'distance': math.sqrt(math.pow(r - grid_row, 2) + math.pow(c - grid_col, 2)),
						'key': poss_key
					}
					available.append(possibility)
		#now find the best available option
		available.sort(key=lambda x: x['distance'])
		if (len(available) > 0):
			best_option = available[0]
			lord['x'] = int(best_option['col'])
			lord['y'] = int(best_option['row'])
			map_grid[best_option['key']] = True

	#get their voting record and bio
	likes = []
	dislikes = []
	lord_page = get_doc("http://www.theyworkforyou.com/peer/" + str(lord['person_id']) + "/votes")
	vote_records = lord_page.find_all("ul", attrs={"class": "vote-descriptions"})
	for ul in vote_records:
		for li in ul.find_all("li"):
			full_text = li.text.strip()
			strength = li.strong.text.strip()
			strength_value = strengths[strength]

			#find where the description starts
			words_list = full_text.split(" ")
			strength_words = strength.split(" ")
			description_start = words_list.index(strength_words[0]) + len(strength_words)

			#deal with 'on' being part of description, which doesn't make sense in isolation
			if (words_list[description_start] == "on"):
				description_start += 1

			#make word, plus tidy up the language/capitals
			description = " ".join(words_list[description_start:-1]).capitalize()
			for replace_word in replace_list:
				description = description.replace(replace_word, replace_list[replace_word])

			#add it to relevant list
			vote = {
				'strength': strength_value,
				'issue': description.strip()
			}
			if (strength_value > 0):
				likes.append(vote)
			else:
				dislikes.append(vote)

	#shuffle list, then sort by strength, and take top three
	random.shuffle(likes)
	random.shuffle(dislikes)
	likes.sort(key=lambda x:x['strength'], reverse=True)
	likes = likes[0:3]
	dislikes.sort(key=lambda x:x['strength'])
	dislikes = dislikes[0:3]

	#add to lord!
	lord['likes'] = likes
	lord['dislikes'] = dislikes

	#load in bio and wikipedia link
	response = requests.get("http://www.theyworkforyou.com/api/getMPInfo?id=" + lord['person_id'] + "&fields=lordbio,wikipedia_url&key=Bf68HrEWZwQtERWhxBEQYfRE")
	content = response.content
	info = json.loads(content)

	if ('wikipedia_url') in info:
		lord['wiki_url'] = info['wikipedia_url'].strip()
	if ('lordbio' in info):
		lord['profile'] = info['lordbio'].strip()

	# #get image for each lord (if there is one)
	# img_url = "http://www.theyworkforyou.com/peer/" + lord['person_id']
	# response = requests.get(img_url)
	# lord_page = BeautifulSoup(response.content)
	# #find image
	# image_div = lord_page.find("div", attrs={"class": "mp-image"})
	# img = image_div.img
	# source_url = img['src']
	# source_file = source_url.split("/")[-1]
	# #save reference to image
	# lord['img'] = source_file
	# #save file
	# if (source_file not in imgs):
	# 	urllib.urlretrieve("http://www.theyworkforyou.com/" + source_url, "./lords_images/" + source_file)
	# 	imgs.append(source_file)

# print the output
print("lords = " + json.dumps(lords))
