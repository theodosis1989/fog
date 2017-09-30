# class Execution:
#     isSuccess = False

class PrivateApplet:
	def __init__(self):
		self.url = ""
		self.data = ""


class CloudBits:
	def __init__(self):
		self.group = ""
		self.value = ""
		self.label = ""

class HueLights:
	def __init__(self):
		self.group = ""
		self.value = ""
		self.label = ""
		self.bri = 100

class MakerWebRequest:
	def __init__(self):
		self.url = ""
		self.method = ""
		self.contenttype = ""
		self.body = ""

class Applet:
	def __init__(self):
		self.text = ""
		self.appletid = ""
		self.triggerChannel = ""
		self.actionChannel = ""
		self.AreLittleBitsUsed = False
		self.AreHueLightsUsed = True
		self.AreExtraFields = False
		self.preSelectedLightValue = ""
		self.preSelectedTriggerValue = ""
		self.preSelectedExtraValue = ""
		self.metaText = ""
		self.mylights = []
		self.mycloudbits = []
		self.isPrivate = False
		self.isPrivate = False