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

lords_count = str(len(lords))

#go through lords one-by-one
for lord in lords:
	#monitor progress
	lord_index = str(lords.index(lord) + 1)
	sys.stderr.write(lord_index + "/" + lords_count + "\n")

#go through lords one-by-one
for lord in lords:
	#monitor progress
	lord_index = str(lords.index(lord) + 1)
	sys.stderr.write(lord_index + "/" + lords_count + "\n")

	#work out if the constituency is more than one work
	constituency_words = lord['constituency'].split(" ")
	if (len(constituency_words) == 1):
		print (lord['wiki_url'] + " *** " + lord['constituency'])
	