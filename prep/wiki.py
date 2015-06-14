import json
from bs4 import BeautifulSoup
import requests
import sys

#missing wiki links
missing_wiki = {
	'Baroness amos': "http://en.wikipedia.org/wiki/Valerie_Amos,_Baroness_Amos",
	'Baroness anelay of st johns': "http://en.wikipedia.org/wiki/Joyce_Anelay,_Baroness_Anelay_of_St_John's",
	'Baroness ashton of upholland': "http://en.wikipedia.org/wiki/Catherine_Ashton",
	'Baroness benjamin': "http://en.wikipedia.org/wiki/Floella_Benjamin,_Baroness_Benjamin",
	'Baroness bonham-carter of yarnbury': "http://en.wikipedia.org/wiki/Jane_Bonham-Carter,_Baroness_Bonham-Carter_of_Yarnbury",
	'Baroness brady': "http://en.wikipedia.org/wiki/Karren_Brady",
	'Baroness brinton': "http://en.wikipedia.org/wiki/Sarah_Brinton,_Baroness_Brinton",
	'Baroness chisholm of owlpen': "http://en.wikipedia.org/wiki/Carlyn_Chisholm,_Baroness_Chisholm_of_Owlpen",
	'Baroness doocey': "http://en.wikipedia.org/wiki/Elizabeth_Doocey,_Baroness_Doocey",
	'Baroness farrington of ribbleton': "http://en.wikipedia.org/wiki/Josie_Farrington,_Baroness_Farrington_of_Ribbleton",
	'Baroness grender': "http://en.wikipedia.org/wiki/Rosalind_Grender,_Baroness_Grender",
	'Baroness hale of richmond': "http://en.wikipedia.org/wiki/Brenda_Hale,_Baroness_Hale_of_Richmond",
	'Baroness heyhoe flint': "http://en.wikipedia.org/wiki/Rachael_Heyhoe_Flint,_Baroness_Heyhoe_Flint",
	'Baroness hilton of eggardon': "http://en.wikipedia.org/wiki/Jennifer_Hilton,_Baroness_Hilton_of_Eggardon",
	'Baroness hussein-ece': "http://en.wikipedia.org/wiki/Meral_Hussein-Ece,_Baroness_Hussein-Ece",
	'Baroness knight of collingtree': "http://en.wikipedia.org/wiki/Jill_Knight",
	'Baroness lawrence of clarendon': "http://en.wikipedia.org/wiki/Doreen_Lawrence,_Baroness_Lawrence_of_Clarendon",
	'Baroness linklater of butterstone': "http://en.wikipedia.org/wiki/Veronica_Linklater,_Baroness_Linklater",
	'Baroness masham of ilton': "http://en.wikipedia.org/wiki/Susan_Cunliffe-Lister,_Baroness_Masham_of_Ilton",
	'Baroness mcintosh of hudnall': "http://en.wikipedia.org/wiki/Genista_McIntosh,_Baroness_McIntosh",
	'Baroness mobarik': "http://en.wikipedia.org/wiki/Nosheena_Mobarik,_Baroness_Mobarik",
	'Baroness neville-rolfe': "http://en.wikipedia.org/wiki/Lucy_Neville-Rolfe,_Baroness_Neville-Rolfe",
	'Baroness nicholson of winterbourne': "http://en.wikipedia.org/wiki/Emma_Nicholson,_Baroness_Nicholson_of_Winterbourne",
	'Baroness nicol': "http://en.wikipedia.org/wiki/Olive_Nicol,_Baroness_Nicol",
	'Baroness nye': "http://en.wikipedia.org/wiki/Susan_Nye,_Baroness_Nye",
	"Baroness o'loan": "http://en.wikipedia.org/wiki/Nuala_O'Loan,_Baroness_O'Loan",
	'Baroness randerson': "http://en.wikipedia.org/wiki/Jennifer_Randerson,_Baroness_Randerson",
	'Baroness suttie': "http://en.wikipedia.org/wiki/Alison_Suttie,_Baroness_Suttie",
	'Baroness vadera': "http://en.wikipedia.org/wiki/Shriti_Vadera,_Baroness_Vadera",
	'Lord allen of kensington': "http://en.wikipedia.org/wiki/Charles_Allen,_Baron_Allen_of_Kensington",
	'Lord archer of weston-super-mare': "http://en.wikipedia.org/wiki/Jeffrey_Archer",
	'Lord barber of tewkesbury': "http://en.wikipedia.org/wiki/Derek_Barber,_Baron_Barber_of_Tewkesbury",
	'Lord berkeley of knighton': "http://en.wikipedia.org/wiki/Michael_Berkeley",
	'Lord black of crossharbour': "http://en.wikipedia.org/wiki/Conrad_Black",
	'Lord blyth of rowington': "http://en.wikipedia.org/wiki/James_Blyth,_Baron_Blyth_of_Rowington",
	'Lord boyd of duncansby': "http://en.wikipedia.org/wiki/Colin_Boyd,_Baron_Boyd_of_Duncansby",
	'Lord bridges': "http://en.wikipedia.org/wiki/Thomas_Bridges,_2nd_Baron_Bridges",
	'Lord briggs': "http://en.wikipedia.org/wiki/Asa_Briggs,_Baron_Briggs",
	'Lord chalfont': "http://en.wikipedia.org/wiki/Alun_Gwynne_Jones,_Baron_Chalfont",
	'Lord clarke of stone-cum-ebony': "http://en.wikipedia.org/wiki/Anthony_Clarke,_Baron_Clarke_of_Stone-cum-Ebony",
	'Lord deighton': "http://en.wikipedia.org/wiki/Paul_Deighton,_Baron_Deighton",
	'Lord farmer': "http://en.wikipedia.org/wiki/Michael_Farmer,_Baron_Farmer",
	'Lord fox': "http://en.wikipedia.org/wiki/Christopher_Fox,_Baron_Fox",
	'Lord goddard of stockport': "http://en.wikipedia.org/wiki/David_Goddard,_Baron_Goddard_of_Stockport",
	'Lord goff of chieveley': "http://en.wikipedia.org/wiki/Robert_Goff,_Baron_Goff_of_Chieveley",
	'Lord grenfell': "http://en.wikipedia.org/wiki/Julian_Grenfell,_3rd_Baron_Grenfell",
	'Lord griffiths': "http://en.wikipedia.org/wiki/Hugh_Griffiths,_Baron_Griffiths",
	'Lord hope of thornes': "http://en.wikipedia.org/wiki/David_Hope,_Baron_Hope_of_Thornes",
	'Lord jenkin of roding': "http://en.wikipedia.org/wiki/Patrick_Jenkin,_Baron_Jenkin_of_Roding",
	'Lord jordan': "http://en.wikipedia.org/wiki/Bill_Jordan,_Baron_Jordan",
	'Lord kerr of tonaghmore': "http://en.wikipedia.org/wiki/Brian_Kerr,_Baron_Kerr_of_Tonaghmore",
	'Lord kilpatrick of kincraig': "http://en.wikipedia.org/wiki/Robert_Kilpatrick,_Baron_Kilpatrick_of_Kincraig",
	'Lord kingsdown': "http://en.wikipedia.org/wiki/Robin_Leigh-Pemberton,_Baron_Kingsdown",
	'Lord lamont of lerwick': "http://en.wikipedia.org/wiki/Norman_Lamont",
	'Lord lennie': "http://en.wikipedia.org/wiki/Christopher_Lennie,_Baron_Lennie",
	'Lord livingston of parkhead': "http://en.wikipedia.org/wiki/Ian_Livingston,_Baron_Livingston_of_Parkhead",
	'Lord macdonald of tradeston': "http://en.wikipedia.org/wiki/Gus_Macdonald",
	'Lord mackay of drumadoon': "http://en.wikipedia.org/wiki/Donald_Mackay,_Baron_Mackay_of_Drumadoon",
	'Lord malloch-brown': "http://en.wikipedia.org/wiki/Mark_Malloch_Brown,_Baron_Malloch-Brown",
	'Lord mance': "http://en.wikipedia.org/wiki/Jonathan_Mance,_Baron_Mance",
	'Lord mason of barnsley': "http://en.wikipedia.org/wiki/Roy_Mason",
	'Lord millett': "http://en.wikipedia.org/wiki/Peter_Millett,_Baron_Millett",
	'Lord moynihan': "http://en.wikipedia.org/wiki/Baron_Moynihan",
	'Lord mustill': "http://en.wikipedia.org/wiki/Michael_Mustill,_Baron_Mustill",
	'Lord neuberger of abbotsbury': "http://en.wikipedia.org/wiki/David_Neuberger,_Baron_Neuberger_of_Abbotsbury",
	'Lord prior': "http://en.wikipedia.org/wiki/James_Prior,_Baron_Prior",
	'Lord prys-davies': "http://en.wikipedia.org/wiki/Gwilym_Prys_Prys-Davies,_Baron_Prys-Davies",
	'Lord richards of herstmonceux': "http://en.wikipedia.org/wiki/David_Richards,_Baron_Richards_of_Herstmonceux",
	'Lord rix': "http://en.wikipedia.org/wiki/Brian_Rix",
	'Lord roberts of conwy': "http://en.wikipedia.org/wiki/Wyn_Roberts,_Baron_Roberts_of_Conwy",
	'Lord sainsbury of preston candover': "http://en.wikipedia.org/wiki/John_Sainsbury,_Baron_Sainsbury_of_Preston_Candover",
	'Lord sainsbury of turville': "http://en.wikipedia.org/wiki/David_Sainsbury,_Baron_Sainsbury_of_Turville",
	'Lord sandberg': "http://en.wikipedia.org/wiki/Michael_Sandberg,_Baron_Sandberg",
	'Lord simon of highbury': "http://en.wikipedia.org/wiki/David_Simon,_Baron_Simon_of_Highbury",
	'Lord simpson of dunkeld': "http://en.wikipedia.org/wiki/George_Simpson,_Baron_Simpson_of_Dunkeld",
	'Lord singh of wimbledon': "http://en.wikipedia.org/wiki/Indarjit_Singh",
	'Lord stirrup': "http://en.wikipedia.org/wiki/Jock_Stirrup,_Baron_Stirrup",
	'Lord thomas of cwmgiedd': "http://en.wikipedia.org/wiki/John_Thomas,_Baron_Thomas_of_Cwmgiedd",
	'Lord thomas of macclesfield': "http://en.wikipedia.org/wiki/Terence_Thomas,_Baron_Thomas_of_Macclesfield",
	'Lord vincent of coleshill': "http://en.wikipedia.org/wiki/Richard_Vincent,_Baron_Vincent_of_Coleshill",
	'Lord williams of baglan': "http://en.wikipedia.org/wiki/Michael_Williams,_Baron_Williams_of_Baglan",
	'Lord williams of oystermouth': "http://en.wikipedia.org/wiki/Rowan_Williams",
	'The bishop of southwark': "http://en.wikipedia.org/wiki/Christopher_Chessun",
	'The duke of norfolk': "http://en.wikipedia.org/wiki/Duke_of_Norfolk",
	'The earl of courtown': "http://en.wikipedia.org/wiki/Patrick_Stopford,_9th_Earl_of_Courtown",
	'The earl of mar and kellie': "http://en.wikipedia.org/wiki/James_Erskine,_Earl_of_Mar_and_Kellie",
	'The earl of shrewsbury': "http://en.wikipedia.org/wiki/Charles_Chetwynd-Talbot,_22nd_Earl_of_Shrewsbury",
	'The earl of snowdon': "http://en.wikipedia.org/wiki/Antony_Armstrong-Jones,_1st_Earl_of_Snowdon",
	'The marquess of cholmondeley': "http://en.wikipedia.org/wiki/David_Cholmondeley,_7th_Marquess_of_Cholmondeley",
	'The marquess of salisbury': "http://en.wikipedia.org/wiki/Robert_Gascoyne-Cecil,_7th_Marquess_of_Salisbury"
}

#load in lords data
lords_file = open("final_lords.json", "r")
lords_data = lords_file.read()
lords_file.close()
lords = json.loads(lords_data[8:])

lords_count = str(len(lords))

#go through lords one-by-one
for lord in lords:
	#monitor progress
	lord_index = str(lords.index(lord) + 1)
	sys.stderr.write(lord_index + "/" + lords_count + "\n")

	#load the page
	if ('wiki_url' in lord):
		wiki_url = lord['wiki_url']

	else:
		wiki_url = missing_wiki[lord['full_name']]
		lord['wiki_url'] = wiki_url

	response = requests.get(wiki_url)
	html = response.content
	wiki_page = BeautifulSoup(html)

	first_para = wiki_page.find(id="mw-content-text").find_next("p").text.strip()
	lord['profile'] = first_para

print("lords = " + json.dumps(lords))