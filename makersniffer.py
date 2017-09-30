# import urllib.request
import urllib2
import time
import datetime
import os
# from scapy.all import *
# import serial
import threading
import datetime
import sqlite3
import json
import urlactions as ua
# from phue import Bridge

mydata = None
token = None
internalIP = None
makerToken = None

# get the maker pair information
with open("jsondata.json") as data_j:
	mydata = json.load(data_j)

# get the hue token and internal ip
with open("huetoken.txt") as f:
	info = f.readline()
	fileinfo = info.split(":")
	internalIP = fileinfo[0]
	token = fileinfo[1]

# not used at the moment
def stopfilterbutton(self):
	if RequestOnIsBack:
		return True

# not used at the moment
def http_header_maker(packet):
	http_packet=bytes(packet)
	http_packet_str = str(http_packet)
	if http_packet_str.find('sendsometext') > 0:
		time = datetime.datetime.now().time()
		global RequestMakerIsBack
		RequestMakerIsBack = True
		print("maker response: %s" % (time))

# maker to maker, offline if there is a pair, online if not
def sniff_maker_requests(url):
	returnValue = 1
	result = None
	time = datetime.datetime.now().time()
	lista = url.split("/")
	print lista[4]
	for x in mydata["public"]["makerKeywords"]["makerPair"]:
		if lista[4] == x["Sent"]:
			print ("Found")
			myval = x["Received"]
			# look in the migrated makers for this keyword
			for y in mydata["public"]["makers"]["maker"]:
				if y["text"] == myval:
					print myval
					print y["url"]
					# do local request
					method_name = getattr(ua, y["url"])
					if not x.has_key("value2"):
						# call with 2 arguments
						result = method_name(y["value1"], token, internalIP)
					else:
						# call with 1 argument
						readesult = method_name(y["value1"], y["value2"], token, internalIP)
					returnValue = 0
		else:
			# call url with keyword and token on iFTTT
			urllib2.urlopen(url).read()
			print ("URL clicked!")
			returnValue = 0
			# sniff(iface='eth0', prn=http_header_maker, filter="tcp port 80", timeout=10, stop_filter=stopfilterbutton)
	return returnValue

RequestOnIsBack = False
RequestMakerIsBack = False