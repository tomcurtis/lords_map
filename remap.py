# -*- coding: utf-8 -*-
#make list of all lords with all info 

import json
import math
import requests
from bs4 import BeautifulSoup
import sys
import random

#map value from left range to right domain
def translate(value, leftMin, leftMax, rightMin, rightMax):
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin

    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)

    # Convert the 0-1 range into a value in the right range.
    return rightMin + (valueScaled * rightSpan)

#load in lords data
lords_file = open("new_lords.json", "r")
lords_data = lords_file.read()
lords_file.close()
lords = json.loads(lords_data)

lords_count = str(len(lords))

#go through lords one-by-one
for lord in lords:
	#monitor progress
	lord_index = str(lords.index(lord) + 1)
	sys.stderr.write(lord_index + "/" + lords_count + "\n")

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

lords_count = str(len(lords))

#go through lords one-by-one
for lord in lords:
	#monitor progress
	lord_index = str(lords.index(lord) + 1)
	sys.stderr.write(lord_index + "/" + lords_count + "\n")

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

print("lords = " + json.dumps(lords))