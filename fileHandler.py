import os

def ReadFromText(filename):
	file = open(filename, "r")
	content = file.readline()
	file.close()
	return content

def WriteToText(filename, content):
	file = open(filename, "w")
	file.write(content)
	file.close()

def ReadFromJSON(filename):
	data_j =  open(filename)
	mydata = json.load(data_j)
	data_j.close()
	return mydata

def WriteToJSON():
	print "still working on it"