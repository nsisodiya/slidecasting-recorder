#!/usr/bin/python
# coding: utf-8

#TODO - FullS&reen
#TODO - Zip
#TODO - Arrow Key Binding
#TODO - Pak&aging

import wx
import os
import commands


#class ODPWindow(wx.Panel):
class ODPWindow():
	
	def __init__(self,parent):
		#wx.Panel.__init__(self, parent, wx.ID_ANY)
		self.panel = parent
		self.panel.Center() # open in the centre of the screen
		self.bitmap = None # set to None as we refer to it in ShowBitmap before we instantiate it
		self.number = 0
		self.total_pages = 0

	def GetCurrentPageNumber(self):
		return self.number + 1;

	def OnAction(self, event, ActionNo):
		print self.number
		print self.total_pages
		
		if ActionNo == "backward":
			if (self.number >= 1):
				self.number = self.number - 1;
				self.Open()
		elif ActionNo == "forward":
			if (self.number < self.total_pages - 1):
				self.number = self.number + 1;
				self.Open()
		
		elif ActionNo == "end":
			self.number = self.total_pages - 1;
			self.Open()
			
		elif ActionNo == "home" :
			self.number = 0;
			self.Open()
		else:
			event.Skip();
			
		self.panel.Refresh()
		
		
	def Open(self):
		filename1 = "/tmp/odpviewer/img" + str(self.number) + ".jpg"
		self.image = wx.Image(filename1, wx.BITMAP_TYPE_ANY, -1) # auto-detect file type		
		self.ShowBitmap()
		
	def OnSize(self, event):
		self.Open()
	def OnOpen(self, event):
		"Open an image file, set title if successful"
		# Create a file-open dialog in the current directory
		
		filters = 'Presentation Files (*.odp)|*.odp'
		#dlg = wx.FileDialog(self.panel, message="Open a ODP file", defaultDir=os.getcwd(), defaultFile="", wildcard=filters, style=wx.OPEN)
		dlg = wx.FileDialog(self.panel, message="Open a ODP file", defaultFile="", wildcard=filters, style=wx.OPEN)
		
		if dlg.ShowModal() == wx.ID_OK:
			# User has selected something, get the path, set the window's title to the path
			filename = dlg.GetPath()
			print filename
			wx.BeginBusyCursor()
			#os.system("./ConvertODP2Images.sh \"" + filename + "\"")
			self.total_pages = int(commands.getoutput('ls /tmp/odpviewer/*.jpg | wc -l'))
			print self.total_pages
			filename1 = "/tmp/odpviewer/img0.jpg"
			self.image = wx.Image(filename1, wx.BITMAP_TYPE_ANY, -1) # auto-detect file type
			self.ShowBitmap()
			wx.EndBusyCursor()
			self.panel.parent.ShowFullScreen(True, style=wx.FULLSCREEN_NOBORDER^wx.FULLSCREEN_NOTOOLBAR^wx.FULLSCREEN_NOMENUBAR^wx.FULLSCREEN_NOSTATUSBAR)
			self.panel.Bind(wx.EVT_SIZE, self.OnSize)

		dlg.Destroy() # we don't need the dialog any more so we ask it to clean-up
		
	def ShowBitmap(self):
		if self.bitmap is not None:
			self.bitmap.Destroy()
		
		# Convert to Bitmap for wxPython to draw it to screen
		bitmap = wx.BitmapFromImage(self.image)
		
		orgheight = bitmap.GetSize().GetHeight()
		orgwidth = bitmap.GetSize().GetWidth()
		orgAspectRatio = float(bitmap.GetSize().GetWidth()) / bitmap.GetSize().GetHeight()
		#print orgAspectRatio
		
		width = self.panel.GetSize()[0]
		height = self.panel.GetSize()[1]
		newAspectRatio = float(width)/height
		#print newAspectRatio
		
		if (newAspectRatio > orgAspectRatio ):
			mulfactor= float(height)/float(orgheight)
			
		else:
			mulfactor= float(width)/float(orgwidth)
		
		image = wx.ImageFromBitmap(bitmap).Scale(orgwidth*mulfactor, orgheight*mulfactor, wx.IMAGE_QUALITY_HIGH)
		ScaledImage = wx.BitmapFromImage(image)

		newPos = ((width - orgwidth)/2,(height-orgheight)/2)
		#print newPos
		
		
		
		self.bitmap = wx.StaticBitmap(self.panel, -1, ScaledImage,pos=newPos)


		# Make the application's window as large as the image
		#self.SetClientSize(self.bitmap.GetSize())
		
		"""height = self.bitmap.GetSize().GetHeight()
		width = self.bitmap.GetSize().GetWidth()
		self.SetClientSize((width, height))
		self.Center() # open in the centre of the screen
		"""
		
		
	def OnClose(self, event):
		os.system("rm -rf /tmp/odpviewer")
		self.Destroy()


if __name__ == "__main__":
	app = wx.App()
	frame = wx.Frame(None,-1)
	panel = wx.Panel(frame,-1,  size=(1900,800)) 
	f = ODPWindow(panel)
	f.Open()
	frame.Show(True)
	app.MainLoop()