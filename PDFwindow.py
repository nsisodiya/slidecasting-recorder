#!/usr/bin/env python
# coding: utf-8

import wx
import wx.lib.wxcairo as wxcairo
import os
import poppler

class PDFWindow(wx.Panel):
	""" This example class implements a PDF Viewer Window, handling Zoom and Scrolling """
	
	def __init__(self, parent):
		wx.Panel.__init__(self, parent, wx.ID_ANY)
		#self.__init__(self, parent, wx.ID_ANY)
		# Wrap a panel inside
		ScrRes = wx.DisplaySize()
		S = (ScrRes[0] *0.95 , ScrRes[1] * 0.95)
		self.panel = wx.Window(self, -1, size=S)
		print self.GetSize()
		# Initialize variables
		self.n_page = 0
		self.scale = 1
		self.document = None
		self.total_pages = None
		self.current_page = None
		self.width = None
		self.height = None
		self.parent = parent
		
	# Connect panel events
		#self.panel.Bind(wx.EVT_PAINT, self.OnPaint)
	def LoadDocument(self, file1):
		self.document = poppler.document_new_from_file("file://"+file1, None)
		#Copy Slides to local
		self.total_pages = self.document.get_n_pages()
		self.current_page = self.document.get_page(self.n_page)
		self.width, self.height = self.current_page.get_size()
		ScrRes = wx.DisplaySize()
		S1 = ( ScrRes[0] / float (self.width ) ) * 0.9
		S2 = ( ScrRes[1] / float (self.height ) ) * 0.9
		print "S1 S2 ", S1 , S2 
		if (S1 < S2 ):
			self.scale = S1
		else:
			self.scale = S2
		print "Scale is --> ", self.scale
		self._UpdateSize()
		self.OnPaint(self)
		self.parent.parent.ShowFullScreen(True, style=wx.FULLSCREEN_NOBORDER^wx.FULLSCREEN_NOTOOLBAR^wx.FULLSCREEN_NOMENUBAR^wx.FULLSCREEN_NOSTATUSBAR)

	def OnPaint(self, event):
#		panel2 = wx.Panel(self, -1, size=(600, 600))
		dc = wx.PaintDC(self.panel)
		cr = wxcairo.ContextFromDC(dc)
		cr.scale(1,1)
		ScrRes = wx.DisplaySize()
		cr.translate(ScrRes[0]*0.15,0) 
		cr.set_source_rgb(1, 1, 1)  # White background
		if self.scale != 1:
			cr.scale(self.scale, self.scale)
		print self.width , self.height
		cr.rectangle(0,0, self.width, self.height)
		cr.fill()
		self.current_page.render(cr)
		

	def _UpdateSize(self):
		#u = PDFWindow.			print(self.width)
		self.SetSize((self.width*self.scale*1.5 , self.height*self.scale*1.1)) #panel.
		#sudo self.SetScrollbars(u, u, (self.width*self.scale)/u, (self.height*self.scale)/u)
	def GetCurrentPageNumber(self):
		return self.n_page
	

	def OnOpen(self, event):
		
		## "Open an image file, set title if successful"
		# Create a file-open dialog in the current directory		
		filters = 'PDF Files (*.pdf)|*.pdf'
		dlg = wx.FileDialog(self, message="Open a PDF file", defaultDir=os.getcwd(),defaultFile="", wildcard=filters, style=wx.OPEN)
		
		if dlg.ShowModal() == wx.ID_OK:
			self.LoadDocument(dlg.GetPath())
			os.system("cp \"" + dlg.GetPath() + "\" ./slides.pdf")
			self.panel.Bind(wx.EVT_PAINT, self.OnPaint)

	def OnAction(self, event,ActionNo):
		
		if ActionNo == "forward":
			next_page = self.n_page + 1
			if (next_page >= 0) and (next_page < self.total_pages):
				self.n_page = next_page
				
		elif ActionNo == "backward":
			next_page = self.n_page - 1
			if (next_page >= 0) and (next_page < self.total_pages):
				self.n_page = next_page
				
		elif ActionNo == "end":
			self.n_page = self.total_pages-1
			
		elif ActionNo == "home" :
			self.n_page = 0
		
		self.current_page = self.document.get_page(self.n_page)
		
		self.Refresh()

				
	def OnClose(self, event):
		dlg = wx.MessageDialog(self,"Do you really want to close this application?","Confirm Exit", wx.OK|wx.CANCEL|wx.ICON_QUESTION)
		result = dlg.ShowModal()
		dlg.Destroy()
		if result == wx.ID_OK:
			self.Destroy()
