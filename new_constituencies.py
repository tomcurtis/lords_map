# -*- coding: utf-8 -*-
#make list of all lords with all info 

import json
import math
import requests
from bs4 import BeautifulSoup
import sys
import random

#load in lords data
lords_file = open("profile_lords.json", "r")
lords_data = lords_file.read()
lords_file.close()
lords = json.loads(lords_data[8:])

#load in new constituency data
constituency_file = open("constituency_check.json", "r")
constituency_lines = constituency_file.readlines()
constituency_file.close()

constituency_list = {}
for line in constituency_lines:
	parts = line.split(" *** ")
	wiki_url = parts[0].strip()
	constituency = parts[1].strip()
	constituency_list[wiki_url] = constituency

lords_count = str(len(lords))

#go through lords one-by-one
for lord in lords:
	#monitor progress
	lord_index = str(lords.index(lord) + 1)
	sys.stderr.write(lord_index + "/" + lords_count + "\n")

	#work out if the constituency is more than one work
	if lord['wiki_url'] in constituency_list:
		lord['constituency'] = constituency_list[lord['wiki_url']]
		
		#get new coordinates from google
		google_url = "https://maps.googleapis.com/maps/api/geocode/json?key=AIzaSyBHWC_9eHNej-xCWGgLKixfx4tpur-0phw&"
		parameters = "region=uk&address=" + lord['constituency'].replace(" ", "+") + "&components=country:GB"
		google_response = requests.get(google_url + parameters)
		google_result = google_response.content
		result = json.loads(google_result)

		lord['lat'] = result['results'][0]['geometry']['location']['lat']
		lord['lon'] = result['results'][0]['geometry']['location']['lng']

print(json.dumps(lords))