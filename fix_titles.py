import json

#load in lords data
lords_file = open("even_finaler_lords.json", "r")
lords_data = lords_file.read()
lords_file.close()
lords = json.loads(lords_data[12:])

#load in titles
titles_file = open("check_titles.txt", "r")
titles_data = titles_file.read()
titles_file.close()
titles = json.loads(titles_data)

#replace old title if found
for lord in lords:
	wiki = lord['wiki_url'].replace("_", " ").replace("%27", "'")
	wiki_parts = wiki.split("/")
	name_part = wiki_parts[-1]

	name_parts = name_part.split(",")
	if (name_parts[0] in titles):
		lord['full_title'] = titles[name_parts[0]]

	lord['full_name'] = lord['full_name'].title()

print("var lords = " + json.dumps(lords, indent=2, sort_keys=True))