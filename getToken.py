import requests
import httplib
import socket
import json
import fileHandler as fh

class Bridge:

	def request(self, mode='GET', address=None):
		""" Utility function for HTTP GET/PUT requests for the API"""
		connection = httplib.HTTPConnection(self.ip, timeout=10)

		try:
			if mode == 'GET' or mode == 'DELETE':
				connection.request(mode, address)
			if mode == 'PUT' or mode == 'POST':
				data1 = {"devicetype": "my_hue_app#random_name"}
				connection.request(mode, address, json.dumps(data1))
				res = connection.getresponse()
				# print (res.read())
			# logger.debug("{0} {1} {2}".format(mode, address, str(data)))
				returndata = str(res.read())
				# print (returndata)
				jsondata = json.loads(returndata)
				if "success" in jsondata[0]:
					return jsondata[0]["success"]["username"]
				else:
					return jsondata[0]["error"]["description"]

		except socket.timeout:
			print ("Exception")
			error = "{} Request to {}{} timed out.".format(mode, self.ip, address)

			# logger.exception(error)
			raise PhueRequestTimeout(None, error)

			result = connection.getresponse()
			connection.close()
			if PY3K:
				return json.loads(str(result.read(), encoding='utf-8'))
			else:
				result_str = result.read()
				logger.debug(result_str)
				return json.loads(result_str)

	# find bridge ip
	def find_bridge(self):
		connection = httplib.HTTPSConnection('www.meethue.com')
		connection.request('GET', '/api/nupnp')
		result = connection.getresponse()
		result_str = result.read()
		result_strj = json.loads(result_str)
		# print result_strj[0]["internalipaddress"]
		fh.WriteToText("huetoken.txt", result_strj[0]["internalipaddress"] + ":")
		# with open("huetoken.txt", "w") as internal_ip_file:
		# 	internal_ip_file.write(result_strj[0]["internalipaddress"] + ":")
		# 	internal_ip_file.close()
		return result_strj[0]["internalipaddress"]

	# find bridge token
	def register_device(self):
		# print (self.ip)
		# connection = httplib.HTTPSConnection(self.ip, timeout=10)
		result = self.request('POST', '/api')
		# print result
		with open("huetoken.txt", "a") as token_file:
			token_file.write(result)
			token_file.close()

	# register_device()
	# find_bridge()

	# registration_request = {"devicetype": "python_hue"}
	# response = self.request('POST', '/api', registration_request)

	def __init__(self):

		bridge_ip = self.find_bridge()
		self.ip = bridge_ip

			# self.minutes = 600 # these do not seem to be used anywhere?
			# self.seconds = 10

		self.register_device()

if __name__ == '__main__':
	Bridge()