import json
import urllib
import urllib2
import requests
import time
from random import randint

def GetLightNumbers(token, ip):
	f = urllib2.urlopen("http://" + str(ip) + "/api/" + str(token) + "/lights")
	fjson = json.loads(f.read())
	return len(fjson)

def TurnOn(light, token, ip):
	dataOn = json.dumps({"on": True, "transitiontime":0, "bri": 254})
	if (light == "all"):
		lampsNum = GetLightNumbers(token, ip)
		for ln in range(1, lampsNum+1):
			print ln
			requests.put("http://" + str(ip) + "/api/" + str(token) + "/lights/" + str(ln) + "/state", data=dataOn)
	else:
		requests.put("http://" + str(ip) + "/api/" + str(token) + "/lights/" + str(light) + "/state", data=dataOn)
	return 0

def TurnOff(light, token, ip):
	dataOff = json.dumps({"on": False, "transitiontime":0, "bri": 254})
	if (light == "all"):
		lampsNum = GetLightNumbers(token, ip)
		for ln in range(1, lampsNum+1):
			requests.put("http://" + str(ip) + "/api/" + str(token) + "/lights/" + str(ln) + "/state", data=dataOff)
	else:
		requests.put("http://" + str(ip) + "/api/" + str(token) + "/lights/" + str(light) + "/state", data=dataOff)
	return 0

def BlinkingLoop(light, token, ip):
	TurnOn(light, token, ip)
	time.sleep(0.3)
	TurnOff(light, token, ip)
	time.sleep(0.3)

def BlinkTheLights(lights, token, ip):
	if (lights == "all"):
		lampsNum = GetLightNumbers(token, ip)
		for counter in range(0, 7):
			for ln in range(1, lampsNum+1):
				BlinkingLoop(ln, token, ip)
	else:
		BlinkingLoop(lights, token, ip)
	return 0

def GetLightsOnStatus(lights, token, ip):
	f = urllib2.urlopen("http://" + str(ip) + "/api/" + str(token) + "/lights/" + str(lights))
	fjson = json.loads(f.read())
	stateOn = fjson["state"]["on"]
	return stateOn

def ToggleLights(lights, token, ip):
	if (lights == "all"):
		lampsNum = GetLightNumbers(token, ip)
		for ln in range(1, lampsNum+1):
			if not GetLightsOnStatus(ln, token, ip):
				TurnOn(int(ln), token, ip)
			else:
				TurnOff(int(ln), token, ip)
	else:
		if not GetLightsOnStatus(lights, token, ip):
			TurnOn(lights, token, ip)
		else:
			TurnOff(lights, token, ip)
	return 0

def SetBrightness(light, percentageValue, token, ip):
	val = (int(percentageValue)*254)/100
	dataBri = json.dumps({"on": True, "transitiontime":0, "bri": val})
	requests.put("http://" + str(ip) + "/api/" + str(token) + "/lights/" + str(light) + "/state", data=dataBri)

def SetColor(light, color, token, ip):
	dataColor = json.dumps({"on": True, "transitiontime":0, "bri": 254, "hue": color})
	requests.put("http://" + str(ip) + "/api/" + str(token) + "/lights/" + str(light) + "/state", data=dataColor)

def DimTheLights(lightsID, briVal, token, ip):
	if (lightsID == "all"):
		lampsNum = GetLightNumbers(token, ip)
		for ln in range(1, lampsNum+1):
			SetBrightness(int(ln), briVal, token, ip)
	else:
		SetBrightness(int(lightsID), briVal, token, ip)
	return 0

def ChangeColor(lightsID, colVal, token, ip):
	if (lightsID == "all"):
		lampsNum = GetLightNumbers(token, ip)
		for ln in range(1, lampsNum+1):
			SetColor(int(ln), int(colVal), token, ip)
	else:
		SetColor(int(lightsID), int(colVal), token, ip)
	return 0

def ChangeToRandomColor(lightsID, token, ip):
	colVal = randint(0, 65000)
	if (lightsID == "all"):
		for ln in range(1, lampsNum+1):
			SetColor(int(ln), colVal, token, ip)
	else:
		SetColor(int(lightsID), colVal, token, ip)
	return 0