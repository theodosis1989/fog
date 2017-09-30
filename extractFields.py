from bs4 import BeautifulSoup
import urllib
import json
from Classes import Applet
from Classes import CloudBits
from Classes import HueLights

def extractPlatformLinks(page):
	soup = BeautifulSoup(page, "html5lib")
	platformLinks = []
	platformURL = "https://platform.ifttt.com"

	# get the URLs of the edit pages
	privateappletsul = soup.find('ul', {'class' : 'web-applet-cards'})

	for privateappletsli in privateappletsul.find_all('li', {'class' : 'web-applet-card'}):
		hlinks = privateappletsli.find('a', {'class' : 'applet-card-body'})
		# print hlinks
		# print ("link1: " + hlinks.get('href'))
		splittedLink = hlinks.get('href').split("/")
		currentURL = platformURL + "/" + splittedLink[1] + "/" + splittedLink[2] + "/" + splittedLink[3] + "/" + splittedLink[4]
		platformLinks.append(currentURL)
	return platformLinks


def returnParams(page, splittedLink):
	soupResponse = BeautifulSoup(page, "html5lib")

	# find token
	metainfo = soupResponse.find('meta', {'name' : 'csrf-token'})
	auth_token = metainfo.get("content")

	params = {'query':'query {applet(id:"' + splittedLink[6] + '") { \n  id\n  name\n  description\n  published\n  archived\n  filter_code\n  channel_id\n\n  applet_trigger {\n    channel_module_name\n    module_name\n\n    fields {\n      name\n      custom_label\n      hidden\n      default_value_json\n    }\n  }\n\n  applet_actions {\n    channel_module_name\n    module_name\n\n    fields {\n      name\n      custom_label\n      hidden\n      default_value_json\n    }\n  }\n }\n  }','authenticity_token':auth_token}

	data = urllib.urlencode(params)

	prApplet = PrivateApplet()
	prApplet.url = "https://platform.ifttt.com/maker/theoshuelights/applets/composer/api/query"
	prApplet.data = data

	return prApplet


def extractPrivateApplets(myjstr):

	CurrentApplets = []
	myapplet = Applet()

	# get the url
	appid = myjstr["applet"]["id"]
	nameApplet = myjstr["applet"]["name"]
	nameApplet = nameApplet.replace(" ", "-")
	urlIndiv = "https://ifttt.com/applets/" + appid + "-" + nameApplet + "/edit"

	# get the filter code
	fcode = myjstr["applet"]["filter_code"]
	# print fcode

	# trigger channel
	inputchannel = myjstr["applet"]["applet_trigger"]["channel_module_name"]
	inputaction = myjstr["applet"]["applet_trigger"]["module_name"]

	if inputchannel == "littlebits" or inputchannel == "maker_webhooks":

		for x in myjstr["applet"]["applet_actions"]:
			myapplet.appletid = appid

			if x["channel_module_name"] == "hue":
				for y in x["fields"]:
					if y["hidden"] == True:
						# TODO: all the hue functionalities must be added here
						if y["name"] == "brightness":
							myapplet.preSelectedExtraValue = y["default_value_json"]
			elif x["channel_module_name"] == "maker_webhooks":
				for y in x["fields"]:
					if y["hidden"] == True:
						if y["name"] == "url":
							myapplet.makerURL = y["default_value_json"]
						if y["name"] == "body":
							myapplet.preSelectedTriggerValue = y["default_value_json"]
		CurrentApplets.append(myapplet)
		return CurrentApplets

def extractUserName(page):
	soup = BeautifulSoup(page, "html5lib")
	selectedDiv = soup.find('div', {'data-react-class' : 'App.Comps.MenuDropdown'})
	selectedString = selectedDiv.get("data-react-props")
	selectedStringJSON = json.loads(selectedString, "r")
	return selectedStringJSON["username"]

def extractMyAppletsLinks(page):
	edit = "/edit"
	soup = BeautifulSoup(page, "html5lib")

	AllApplets = []

	ulmain = soup.find('ul', {'class' : 'web-applet-cards'})
	for liapplets in ulmain.find_all('li', {'class' : 'my-web-applet-card'}):
		myapplet = Applet()
		isHueAsAction = False
		isMakerAction = False
		isAppletOn = False
		isMakerTrigger = False
		isLbTrigger = False
		isDateTimeTrigger = False
		isLIFXAction = False

		# see if it is private
		privateTag = liapplets.find('svg', {'class':'private-icon'})
		if(privateTag is None):

			# show only applets that have as trigger either LB or Maker
			for imgtrigger in liapplets.find_all('img', {'class' : 'owner-logo'}):
				if imgtrigger.get('title') == "littleBits":
					isLbTrigger = True
				elif imgtrigger.get('title') == "Webhooks":
					isMakerTrigger = True
				 # exception for datetime - hue applet, icons are wrong
				elif imgtrigger.get('title') == "Philips Hue":
					isHueAsAction = True

			# show only Applets with Philips Hue or Maker as action
			metaClass = liapplets.find('div', {'class':'meta'})
			workswith = metaClass.find('ul', {'class': 'permissions'})
			if(workswith is not None):
				linside = workswith.find('li')
				imgaction = linside.find('img')
				# print (imgaction.get("title"))
				if imgaction.get("title") == "Philips Hue":
					isHueAsAction = True
				# exception for datetime - hue applet, icons are wrong
				elif imgaction.get("title") == "Date & Time":
					isDateTimeTrigger = True
				elif imgaction.get("title") == "LIFX":
					isLIFXAction = True
			else:
				isMakerAction = True

			for statusled in liapplets.find_all('div', {'class': 'status'}):
				if statusled.text.strip() == "On":
					isAppletOn = True

			if (isHueAsAction or isMakerAction) and isAppletOn and (isLbTrigger or isMakerTrigger or isDateTimeTrigger):

				imgtrigger = liapplets.find('img', {'class' : 'owner-logo'})

				# this if is used to fix this anomaly with ifttt having the wrong logos for datetime - hue applet
				if (imgtrigger.get('title') == "Philips Hue") and isDateTimeTrigger:
					myapplet.triggerChannel = "Date & Time"
				else:
					myapplet.triggerChannel = imgtrigger.get('title')

				# if imgtrigger.get('title') == "littleBits":
				# 	myapplet.triggerChannel = "littleBits"
				# elif imgtrigger.get('title') == "Maker Webhooks":	
				# 	myapplet.triggerChannel = "Maker Webhooks"

				if isMakerAction:
					myapplet.actionChannel = "Webhooks"
				elif isHueAsAction:
					myapplet.actionChannel = "Philips Hue"
				elif isLIFXAction:
					myapplet.actionChannel = "LIFX"

				hlink = liapplets.find('a', {'class' : 'applet-card-body'})
				hlinkedit = hlink.get('href') + edit
				myapplet.appletURL = hlinkedit
				AllApplets.append(myapplet)
	return AllApplets

# save the ifttt maker token on a file
def extractMakerSettings(page):
	ddcounter = 0
	iftttToken = None
	soup = BeautifulSoup(page, "html5lib")
	settingsli = soup.find('li', {'class':'setting-box'})
	dlpart = settingsli.find('dl')
	for ddpart in dlpart.find_all('dd'):
		if(ddcounter == 1):
			iftttToken = ddpart.text.split("/")
			# print iftttToken[4]
			with open("iftttMakerToken.txt", "w") as f:
				f.write(iftttToken[4])
				f.close()
		ddcounter+=1

def returnCSRFTokenFromSoup(soup):
	# find token
	# soup = BeautifulSoup(page, "html5lib")
	metainfo = soup.find('meta', {'name' : 'csrf-token'})
	auth_token = metainfo.get("content")
	return auth_token

def returnCSRFTokenFromPage(page):
	# find token
	soup = BeautifulSoup(page, "html5lib")
	metainfo = soup.find('meta', {'name' : 'csrf-token'})
	auth_token = metainfo.get("content")
	return auth_token


def extractAllAppletsEditPages(page, myapplet, lampsJSON, littlebitsJSON):

	soup = BeautifulSoup(page, "html5lib")

	appletid = soup.find('p', {'class':'applet-id'})
	appletcode = appletid.text.strip()

	myapplet.appletid = appletcode
	metaText = ""

	# find the pre selected Values for the DropDown Lists
	selectedDiv = soup.find('div', {'data-react-class' : 'App.Comps.AppletStoredFieldsForm'})
	selectedString = selectedDiv.get("data-react-props")
	selectedStringJSON = json.loads(selectedString, "r")
	# print (selectedStringJSON)
	# print "=================================="
	applettext = selectedStringJSON["applet"]["name"]
	trigVal = selectedStringJSON["storedFields"][0]["value"]
	trigLbl = selectedStringJSON["storedFields"][0]["label"]
	myapplet.triggerLabel = trigLbl.strip()
	myapplet.preSelectedTriggerValue = trigVal.strip()
	if lampsJSON is not None:

		lampsCount = len(lampsJSON["lights"])

		for hiter in range(lampsCount):
			huelights = HueLights()
			huelights.group = lampsJSON["lights"][hiter]["group"]
			huelights.value = lampsJSON["lights"][hiter]["value"]
			huelights.label = lampsJSON["lights"][hiter]["label"]
			myapplet.mylights.append(huelights)

	if littlebitsJSON is not None:

		cbitsCount = len(littlebitsJSON["device_id"])

		for citer in range(cbitsCount):
			cbits = CloudBits()
			cbits.label = littlebitsJSON["device_id"][citer]["label"]
			cbits.value = littlebitsJSON["device_id"][citer]["value"]
			cbits.group = littlebitsJSON["device_id"][citer]["group"]
			myapplet.mycloudbits.append(cbits)

	if myapplet.isPrivate == False:

		actVal = selectedStringJSON["storedFields"][1]["value"]
		actLbl = selectedStringJSON["storedFields"][1]["label"]
		actURL = ""
		metaText = selectedStringJSON["ingredientsMetadata"]["trigger"]["name"]

		if (len(selectedStringJSON["storedFields"]) == 3):
			myapplet.AreExtraFields = True
			extraActLbl = selectedStringJSON["storedFields"][2]["label"]
			extraActVal = selectedStringJSON["storedFields"][2]["value"]
			myapplet.preSelectedExtraValue = extraActVal.strip()
			myapplet.extraLabel = extraActLbl.strip()

		if myapplet.actionChannel == "Webhooks":
			actVal = selectedStringJSON["storedFields"][4]["value"]
			actLbl = selectedStringJSON["storedFields"][4]["label"]
		else:
			actVal = selectedStringJSON["storedFields"][1]["value"]
			actLbl = selectedStringJSON["storedFields"][1]["label"]

		myapplet.text = applettext
		myapplet.metaText = metaText
		myapplet.preSelectedLightValue = actVal
		myapplet.actionLabel = actLbl.strip()
		myapplet.makerURL = actURL
	return myapplet