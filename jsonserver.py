import json
import web
import fileHandler as fh
import urlactions as ua
import makersniffer as ms

mydata = None
token = None
internalIP = None

# with open("test_jdata.json") as data_j:
with open("jsondata.json") as data_j:
	mydata = json.load(data_j)
	data_j.close()

info = fh.ReadFromText("huetoken.txt")
fileinfo = info.split(":")
internalIP = fileinfo[0]
token = fileinfo[1]

# get the maker token
with open("iftttMakerToken.txt") as mf:
	makerToken = mf.readline()

urls = (
	'/public/lamps', 'list_lamps',
	'/public/makers', 'list_makers',
	'/public/cloudbits', 'list_cloudbits',
	'/public/makers/(.*)', 'maker_action_two_args',
	'/public/makersextra/(.*)/(.*)/(.*)', 'maker_action_three_args',
	'/public/appletbylamp/(.*)', 'get_applet_by_lamp',
	'/public/appletbycloudbit/(.*)', 'get_applet_by_cloudbit'
)

app = web.application(urls, globals())

# run maker functions
class maker_action_two_args:
	def GET(self, funcname):
		for x in mydata["public"]["makers"]["maker"]:
			if x["text"] == funcname:
				if not x.has_key("value2"):
					method_name = getattr(ua, x["url"])
					result = method_name(x["value1"], token, internalIP)
				else:
					method_name = getattr(ua, x["url"])
					result = method_name(x["value1"], x["value2"], token, internalIP)
				return result
		# name does not exist in maker to hue, looks at makers to makers
		url = "https://maker.ifttt.com/trigger/" + str(funcname) + "/with/key/" + str(makerToken)
		print url
		return ms.sniff_maker_requests(url)


# not used
class maker_action_three_args:
	def GET(self, funcname, arg1, arg2):
		for x in mydata["public"]["makers"]["maker"]:
			if x["text"] == funcname:
				method_name = getattr(ua, x["url"])
				result = method_name(arg1, arg2)
				return result

# list the lamps
class list_lamps:        
	def GET(self):
		lamps = []
		for timerlamp in mydata["public"]["timers"]["timer"]:
			for a in timerlamp["lamps"]["lights"]:
				lamps.append(a["label"])
		for makerlamps in mydata["public"]["makers"]["maker"]:
			for b in makerlamps["lamps"]["lights"]:
				lamps.append(b["label"])
		for cloudbitlamps in mydata["public"]["cloudbits"]["cloudbit"]:
			for c in cloudbitlamps["lamps"]["lights"]:
				lamps.append(c["label"])
		myLampSet = set(lamps)
		return myLampSet

# list applets that use the cloudbit
class get_applet_by_cloudbit:
	def GET(self, name):
		applets = []
		for cloudbits in mydata["public"]["cloudbits"]["cloudbit"]:
			for c in cloudbits["littleBits"]["device_id"]:
				if c["label"] == name:
					applets.append(cloudbits["function"])
			return applets

# list applets by the lamps
class get_applet_by_lamp:
	def GET(self, name):
		applets = []
		for timerlamp in mydata["public"]["timers"]["timer"]:
			for a in timerlamp["lamps"]["lights"]:
				if a["label"] == name:
					applets.append(timerlamp["function"])
		for makerlamps in mydata["public"]["makers"]["maker"]:
			for b in makerlamps["lamps"]["lights"]:
				if b["label"] == name:
					applets.append(makerlamps["function"])
		for cloudbitlamps in mydata["public"]["cloudbits"]["cloudbit"]:
			for c in cloudbitlamps["lamps"]["lights"]:
				if c["label"] == name:
					applets.append(cloudbitlamps["function"])
		myLampApplets = set(applets)
		return myLampApplets

# list cloudbits
class list_cloudbits:
	def GET(self):
		cbs = []
		for cloudbits in mydata["public"]["cloudbits"]["cloudbit"]:
			for c in cloudbits["littleBits"]["device_id"]:
				cbs.append(c["label"])
		myCBSet = set(cbs)
		return myCBSet

# list makers
class list_makers:
	def GET(self):
		make = []
		for c in mydata["public"]["makers"]["maker"]:
			make.append(c["text"])
		myMakeSet = set(make)
		return myMakeSet



if __name__ == "__main__":
	app.run()