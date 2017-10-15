import urlactions as ua

def Worker_Lock(light, token, ip, lock, url, dimVal, method_name):
	if dimVal == None:
		method_name(light, token, ip)
	else:
		method_name(light, dimVal, token, ip)

	lock.acquire()
	if url == 'TurnOff':
		ua.UpdateShadow(light, True, False, ua.GetLightBrightness(light, token, ip))
	elif url == 'TurnOn':
		ua.UpdateShadow(light, True, True, 254)
	elif url == 'DimTheLights':
		print "update shadow for dim"
		ua.UpdateShadow(light, True, True, dimVal)
	elif url == 'ToggleLights':
		ua.UpdateShadow(light, True, ua.GetLightsOnStatus(light, token, ip))
	lock.release()