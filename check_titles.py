import json

#load in lords data
lords_file = open("new_new_lords.json", "r")
lords_data = lords_file.read()
lords_file.close()
lords = json.loads(lords_data[8:])

new_names = []

for lord in lords:
	wiki = lord['wiki_url'].replace("_", " ").replace("%27", "'")
	wiki_parts = wiki.split("/")
	name_part = wiki_parts[-1]

	name_parts = name_part.split(",")
	if (len(name_parts) > 1):
		title_part = name_parts[1].strip()
		lord['full_title'] = title_part

		if ((" of " not in title_part) and ("1st" not in title_part) and ("2nd" not in title_part) and ("3rd" not in title_part) and ("4th" not in title_part) and ("5th" not in title_part) and ("6th" not in title_part) and ("7th" not in title_part) and ("8th" not in title_part) and ("9th" not in title_part) and ("0th" not in title_part) and ("1th" not in title_part) and ("2th" not in title_part) and ("3th" not in title_part)):
			new_names.append(name_parts[0])
		
	else:
		if ((name_parts[0][:9] == "Bishop of") or (name_parts[0][:13] == "Archbishop of")):
			lord['full_title'] = name_parts[0]

		else:
			lord['full_title'] = name_parts[0]
			new_names.append(name_parts[0])

print(json.dumps(lords))

# for line in new_names:
# 	print ('"' + line + '": ' + "")


