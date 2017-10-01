import mechanize
import cookielib
from bs4 import BeautifulSoup
import html2text
import requests
import sys
import re
import time
import json
import os
import urllib
import urllib2
reload(sys)
sys.setdefaultencoding('utf-8')
from Classes import Applet
from Classes import CloudBits
from Classes import HueLights
import extractFields as ef
import createFile as cf
# from Classes import Execution
sizetotal = 0
start_time = None

# execute the mechanize request to retrieve the requested page and calculating total size of downloaded data
def mechanizeRequest(br, url):
	page = None
	try:
		page = br.open(url).read()
		datasize = len(page)
		global sizetotal
		sizetotal += datasize
		# print sizetotal
	except (mechanize.HTTPError, mechanize.URLError):
		print ("Error, trying again...")
		ScrapeIFTTT()
	return page

# get bridge internal ip and token into the text file
def fetchToken():
	import getToken as gt
	gt.Bridge()

def checkTokenFile():
	f = open("huetoken.txt")
	info = f.readline()
	isReady = False
	if not(("link button not pressed" in info) or (os.stat("huetoken.txt").st_size < 3)):
		isReady = True
	return isReady

def fetchCredentials():
	print "getCred"
	f = open("credentials.txt")
	info = f.readline()
	print info
	fileinfo = info.split(":")
	userName = fileinfo[0]
	print userName
	password = fileinfo[1]
	print password
	f.close()

#start scraping
def ScrapeIFTTT():
	# get internal IP and token of the hue bridge
	while 1:
		if (checkTokenFile()):
			break
		fetchToken()
		print "press bridge button"
		time.sleep(3)

	fetchCredentials()
	fillShadowFile()

	#start timer
	print "Scraping..."
	start_time = time.time()

	# Browser
	br = mechanize.Browser()

	# Cookie Jar
	cj = cookielib.LWPCookieJar()
	br.set_cookiejar(cj)

	# Browser options
	br.set_handle_equiv(True)
	br.set_handle_gzip(True)
	br.set_handle_redirect(True)
	br.set_handle_referer(True)
	br.set_handle_robots(False)
	br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

	br.addheaders = [('User-agent', 'Chrome')]

	# go to the login page
	try:
		br.open('https://ifttt.com/login')
	except (mechanize.HTTPError, mechanize.URLError):
		print("error login, trying again...")
		ScrapeIFTTT()

	br.select_form(nr=0)

	# User credentials
	br.form['user[username]'] = ''
	br.form['user[password]'] = ''

	# Login
	try:
		br.submit()
	except (mechanize.HTTPError, mechanize.URLError):
		print ("Error, trying again...")
		ScrapeIFTTT()

	# navigate to myapplets page
	myappletspage = mechanizeRequest(br, 'https://ifttt.com/my_applets')
	
	# AllApplets variable contains the links of the to be-scraped applets
	AllApplets = ef.extractMyAppletsLinks(myappletspage)

	# extract ifttt username
	username = ef.extractUserName(myappletspage)

	platformLinks = []
	CurrentApplets = []

	# get ifttt platfrom information (it will be used to migrate private applets - not used now)
	platformResponseLink = "https://platform.ifttt.com/maker/" + username + "/applets/private"
	platformresponse = mechanizeRequest(br, platformResponseLink)
	platformLinks = ef.extractPlatformLinks(platformresponse)

	makerSettings = "https://ifttt.com/services/maker_webhooks/settings"
	makerSettingsResponse = mechanizeRequest(br, makerSettings)
	ef.extractMakerSettings(makerSettingsResponse)
	
	counter = 0
	lampsJson = None
	lbsJson = None

	for currApp in AllApplets:

		myapplet = Applet()
		mylink = currApp.appletURL

		htmlresponse = None
		htmlresponse = mechanizeRequest(br, mylink)

		# get littleBits
		if currApp.triggerChannel == "littleBits":
			# get auth_token
			auth_token = ef.returnCSRFTokenFromPage(htmlresponse)
			# get all the lights
			urlGetHue = 'https://ifttt.com/stored_fields/options?resolve_url=/sdk/stored_fields/actions/hue.blink_all_hue/lights/options&authenticity_token=' + auth_token
			resp = mechanizeRequest(br, urlGetHue)
			lampsJson = json.loads(resp)
			

		# get lights
		if currApp.AreHueLightsUsed == True:
			# get auth_token
			auth_token = ef.returnCSRFTokenFromPage(htmlresponse)
			# get all cloudbits
			urlGetLB = 'https://ifttt.com/stored_fields/options?resolve_url=/sdk/stored_fields/triggers/littlebits.ignite/device_id/options&authenticity_token=' + auth_token
			resp = mechanizeRequest(br, urlGetLB)
			lbsJson = json.loads(resp)
			currApp.AreLittleBitsUsed = True

		# extract information for all availables applets
		currentApplet = ef.extractAllAppletsEditPages(htmlresponse, currApp, lampsJson, lbsJson)
		CurrentApplets.append(currentApplet)
	
	appletssize = len(CurrentApplets)
	for it in range(appletssize):
		print ("trigger channel: " + CurrentApplets[it].triggerChannel)
		print ("trigger label: " + CurrentApplets[it].triggerLabel)
		if not CurrentApplets[it].isPrivate:
			print ("action channel: " + CurrentApplets[it].actionChannel)
			print ("action label: " + CurrentApplets[it].actionLabel)
		else:
			for ch in CurrentApplets[it].privateActions:
				print ("action channel: " + ch)
			for ch in CurrentApplets[it].privateLabelsText:
				print ("action labels : " + ch)
		print ("text: " + CurrentApplets[it].text)
		print ("applet-id: " + CurrentApplets[it].appletid)
		print ("selected trigger: " + CurrentApplets[it].preSelectedTriggerValue)
		print ("maker URL: " + CurrentApplets[it].makerURL)
		if CurrentApplets[it].AreLittleBitsUsed == True:
			cblen = len(CurrentApplets[it].mycloudbits)
			for itcb in range(cblen):
				print ("label: " + CurrentApplets[it].mycloudbits[itcb].label)
				print ("value: " + CurrentApplets[it].mycloudbits[itcb].value)
				print (CurrentApplets[it].mycloudbits[itcb].group)
		if CurrentApplets[it].AreHueLightsUsed == True:
			print ("selected lights: " + CurrentApplets[it].preSelectedLightValue)
			huelen = len(CurrentApplets[it].mylights)
			for ithue in range(huelen):
				print ("label: " + CurrentApplets[it].mylights[ithue].label)
				print ("value: " + CurrentApplets[it].mylights[ithue].value)
				print (CurrentApplets[it].mylights[ithue].group)
		if CurrentApplets[it].AreExtraFields == True:
			print ("label: " + CurrentApplets[it].extraLabel)
			print ("value: " + CurrentApplets[it].preSelectedExtraValue)
		print ("==========================================================")
	
	# add applets to file
	cf.importApplets(CurrentApplets, lampsJson, lbsJson)

	elapsed_time = time.time() - start_time
	print elapsed_time
	return True

while(not ScrapeIFTTT()):
	print ("trying again...")
print ("finished")
