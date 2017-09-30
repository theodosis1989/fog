import json


def importApplets(CurrentApplets, lamps, littlebs):

	dataToStore = {	'public': {	'makers': {	'maker': []	},'cloudbits': {'cloudbit': [] }, 'timers': { 'timer': [] }, 'makerKeywords': {	'makerPair': []	} } }

	try:
		with open("jsondata.json", "w") as f:
			appletssize = len(CurrentApplets)
			for it in range(appletssize):
				# print (CurrentApplets[it].text)
				if (CurrentApplets[it].isPrivate == False):
					if (CurrentApplets[it].triggerChannel == "littleBits"):
						if("Blink" in CurrentApplets[it].text):
							dataToStore["public"]["cloudbits"]["cloudbit"].append({"appletid":CurrentApplets[it].appletid, "metadataText": CurrentApplets[it].metaText, "cloudbit": CurrentApplets[it].preSelectedTriggerValue, "text": "text", "url": "BlinkTheLights", "function": "Blink The Lights", "value1": CurrentApplets[it].preSelectedLightValue, "littleBits":littlebs, "lamps":lamps})
						elif("toggle" in CurrentApplets[it].text):
							dataToStore["public"]["cloudbits"]["cloudbit"].append({"appletid":CurrentApplets[it].appletid, "metadataText": CurrentApplets[it].metaText, "cloudbit": CurrentApplets[it].preSelectedTriggerValue, "text": "text", "url": "ToggleLights", "function": "Toggle The Lights", "value1": CurrentApplets[it].preSelectedLightValue, "littleBits":littlebs, "lamps":lamps})
						elif("turn on" in CurrentApplets[it].text):
							dataToStore["public"]["cloudbits"]["cloudbit"].append({"appletid":CurrentApplets[it].appletid, "metadataText": CurrentApplets[it].metaText, "cloudbit": CurrentApplets[it].preSelectedTriggerValue, "text": "text", "url": "TurnOn", "function": "Turn On The Lights", "value1": CurrentApplets[it].preSelectedLightValue, "littleBits":littlebs, "lamps":lamps})
						elif("turn off" in CurrentApplets[it].text):
							dataToStore["public"]["cloudbits"]["cloudbit"].append({"appletid":CurrentApplets[it].appletid, "metadataText": CurrentApplets[it].metaText, "cloudbit": CurrentApplets[it].preSelectedTriggerValue, "text": "text", "url": "TurnOff", "function": "Turn Off The Lights", "value1": CurrentApplets[it].preSelectedLightValue, "littleBits":littlebs, "lamps":lamps})
						elif("then dim" in CurrentApplets[it].text):
							dataToStore["public"]["cloudbits"]["cloudbit"].append({"appletid":CurrentApplets[it].appletid, "metadataText": CurrentApplets[it].metaText, "cloudbit": CurrentApplets[it].preSelectedTriggerValue, "text": "text", "url": "DimTheLights", "function": "Dim The Lights", "value1": CurrentApplets[it].preSelectedLightValue, "value2": CurrentApplets[it].preSelectedExtraValue, "littleBits":littlebs, "lamps":lamps})
					elif(CurrentApplets[it].triggerChannel == "Webhooks"):
						if("Blink" in CurrentApplets[it].text):
							dataToStore["public"]["makers"]["maker"].append({"appletid":CurrentApplets[it].appletid, "what": CurrentApplets[it].metaText, "text": CurrentApplets[it].preSelectedTriggerValue, "url": "BlinkTheLights", "function": "Blink The Lights", "value1": CurrentApplets[it].preSelectedLightValue, "lamps":lamps})
						elif("toggle" in CurrentApplets[it].text):
							dataToStore["public"]["makers"]["maker"].append({"appletid":CurrentApplets[it].appletid, "what": CurrentApplets[it].metaText, "text": CurrentApplets[it].preSelectedTriggerValue, "url": "ToggleLights", "function": "Toggle The Lights", "value1": CurrentApplets[it].preSelectedLightValue, "lamps":lamps})
						elif("turn on" in CurrentApplets[it].text):
							dataToStore["public"]["makers"]["maker"].append({"appletid":CurrentApplets[it].appletid, "what": CurrentApplets[it].metaText, "text": CurrentApplets[it].preSelectedTriggerValue, "url": "TurnOn", "function": "Turn On The Lights", "value1": CurrentApplets[it].preSelectedLightValue, "lamps":lamps})
						elif("turn off" in CurrentApplets[it].text):
							dataToStore["public"]["makers"]["maker"].append({"appletid":CurrentApplets[it].appletid, "what": CurrentApplets[it].metaText, "text": CurrentApplets[it].preSelectedTriggerValue, "url": "TurnOff", "function": "Turn Off The Lights", "value1": CurrentApplets[it].preSelectedLightValue, "lamps":lamps})
						elif("then dim" in CurrentApplets[it].text):
							dataToStore["public"]["makers"]["maker"].append({"appletid":CurrentApplets[it].appletid, "what": CurrentApplets[it].metaText, "text": CurrentApplets[it].preSelectedTriggerValue, "url": "DimTheLights", "function": "Dim The Lights", "value1": CurrentApplets[it].preSelectedLightValue, "value2": CurrentApplets[it].preSelectedExtraValue, "lamps":lamps})
						elif(CurrentApplets[it].actionChannel == "Webhooks"):
							# dataToStore["ifttt"]["makers"]["maker"].append({"what": CurrentApplets[it].metaText, "text": CurrentApplets[it].preSelectedTriggerValue, "url": "....", "function": "Make a Request", "value1": CurrentApplets[it].preSelectedLightValue})
							dataToStore["public"]["makerKeywords"]["makerPair"].append({"appletid":CurrentApplets[it].appletid, "Sent": CurrentApplets[it].preSelectedTriggerValue, "Received": CurrentApplets[it].preSelectedLightValue})
					elif(CurrentApplets[it].triggerChannel == "Date & Time"):
						if("Blink" in CurrentApplets[it].text):
							dataToStore["public"]["timers"]["timer"].append({"appletid":CurrentApplets[it].appletid, "when": CurrentApplets[it].metaText, "text": CurrentApplets[it].preSelectedTriggerValue, "url": "BlinkTheLights", "function": "Blink The Lights", "value1": CurrentApplets[it].preSelectedLightValue, "lamps":lamps})
						elif("toggle" in CurrentApplets[it].text):
							dataToStore["public"]["timers"]["timer"].append({"appletid":CurrentApplets[it].appletid, "when": CurrentApplets[it].metaText, "text": CurrentApplets[it].preSelectedTriggerValue, "url": "ToggleLights", "function": "Toggle The Lights", "value1": CurrentApplets[it].preSelectedLightValue, "lamps":lamps})
						elif("turn on" in CurrentApplets[it].text):
							dataToStore["public"]["timers"]["timer"].append({"appletid":CurrentApplets[it].appletid, "when": CurrentApplets[it].metaText, "text": CurrentApplets[it].preSelectedTriggerValue, "url": "TurnOn", "function": "Turn On The Lights", "value1": CurrentApplets[it].preSelectedLightValue, "lamps":lamps})
						elif("turn off" in CurrentApplets[it].text):
							dataToStore["public"]["timers"]["timer"].append({"appletid":CurrentApplets[it].appletid, "when": CurrentApplets[it].metaText, "text": CurrentApplets[it].preSelectedTriggerValue, "url": "TurnOff", "function": "Turn Off The Lights", "value1": CurrentApplets[it].preSelectedLightValue, "lamps":lamps})
						elif("then dim" in CurrentApplets[it].text):
							dataToStore["public"]["timers"]["timer"].append({"appletid":CurrentApplets[it].appletid, "when": CurrentApplets[it].metaText, "text": CurrentApplets[it].preSelectedTriggerValue, "url": "DimTheLights", "function": "Dim The Lights", "value1": CurrentApplets[it].preSelectedLightValue, "value2": CurrentApplets[it].preSelectedExtraValue, "lamps":lamps})
			json.dump(dataToStore, f)
			return True

	except IOError:
		print ("IOError4 trying again...")
		# ScrapeIFTTT()