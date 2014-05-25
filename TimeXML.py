#!/usr/bin/python

#(c) 2011 , Narendra Sisodiya , narendra@narendrasisodiya.com
#   Released under GPLv3
#   <eduvid>
#	<click page="2" time="12"> </click>
#    </eduvid>
#
#


import xml.dom.minidom

class TimeXML:
	def __init__(self):
		self.xmldoc = xml.dom.minidom.parseString("<eduvid></eduvid>")

	def PrintXML(self):
		print str(self.xmldoc.toxml())

	def GetXML(self):
		return str(self.xmldoc.toprettyxml())
	
	def SaveXML(self,filename):
		NewFile = open(filename,"w")
		NewFile.write(self.GetXML())
		NewFile.close()
	def InsertMostBasicClickNode(self,timevalue,page):
		click = self.xmldoc.createElement("click")
		click.setAttribute("time",str(timevalue))
		click.setAttribute("page",str(page))
		self.xmldoc.firstChild.appendChild(click)

'''
testdoc = TimeXML()
testdoc.InsertMostBasicClickNode("1","1")
testdoc.InsertMostBasicClickNode("2","2")
testdoc.PrintXML()
'''
