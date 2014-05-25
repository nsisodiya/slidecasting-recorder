#!/usr/bin/env python
# coding: utf-8
"""
	Slidecasting Recorder, a Product of Elpa Corp. www.elpacorp.com
	Copyright (c) 2011 , Narendra Sisodiya , narendra@narendrasisodiya.com www.elpacorp.com
	Released under GPLv3
	Visit - http://code.google.com/p/slidecasting-recorder to know more about team

	Dependency -
		sudo apt-get install python-poppler python-wxgtk2.8 unoconv gst


"""

import wx
import os
import PDFwindow
import wx.html
import wx.lib.wordwrap
import PythonTimer
import TimeXML
import PythonGstreamerAudioRecorder
import ODPwindow
import WxWebcamTest


pgsar = PythonGstreamerAudioRecorder.PythonGstreamerAudioRecorder()
audioDeviceId = 0

class EduVidAbout(wx.Frame):
	"""This Slidecas"""

	text = '''<html>
		<h1>Slidecasting Recorder</h1>
		<p>It is a presentation application. You can use ODP (Libreoffice) and PDF files. When you start recording a presetation. It will mix your Audio and Slide into one</p>
		<p>Developed at Elpa Technologies </p>
		<p>Official Website <a href="http://www.narendrasisodiya.com">Narendra Sisodiya, Elpa Technologies</a>.</p>
		</html>'''

	def __init__(self, parent):
		wx.Frame.__init__(self, parent, -1, 'About this', size=(550,350))
		info = wx.AboutDialogInfo()
		info.Name = "Eduvid Recorder"
		info.Version = "0.1"
		info.Copyright = "(C) 2011 Narendra Sisodiya, ELPA Technologies, India \n http://elpacorp.com"
		info.Description = wx.lib.wordwrap.wordwrap(
			"A \"hello world\" program is a software program that prints out "
            "\"Hello world!\" on a display device. It is used in many introductory "
            "tutorials for teaching a programming language."
            
            "\n\nSuch a program is typically one of the simplest programs possible "
            "in a computer language. A \"hello world\" program can be a useful "
            "sanity test to make sure that a language's compiler, development "
            "environment, and run-time environment are correctly installed.",
            350, wx.ClientDC(self))
		info.WebSite = ("http://elpacorp.com", "ELPA Technologies")
		info.Developers = [ "Narendra Sisodiya"]
		info.License = wx.lib.wordwrap.wordwrap("GPLv3", 500, wx.ClientDC(self))

		# Then we call wx.AboutBox giving it that info object
		wx.AboutBox(info)


class PreferencesDialog(wx.Frame):
	"""This Slidecas"""

	def __init__(self, parent, ID, title, pos=wx.DefaultPosition,size=(600,300),style=wx.DEFAULT_FRAME_STYLE):
		wx.Frame.__init__(self, parent, ID, title, pos, size, style)
		panel = wx.Panel(self, -1)
		self.statusBar = self.CreateStatusBar()
		
		listDevices = os.popen("arecord -l | grep card").readlines()
		
		y = 20
		x = 20

		wx.StaticText(panel, -1, 'Audio Cards :', (x,y))
		y = y + 20
		for line in listDevices:
			wx.StaticText(panel, -1, line, (x+30,y))
			y=y+20

		
		y=y+5
		
		wx.StaticLine(panel, -1, pos=(x,y), size=wx.Size(560,7), style=wx.LI_HORIZONTAL)
		y=y+15
		
		wx.StaticText(panel, -1, 'Select Card : \n\n\t\t (most of the case, 0 works well)', (x,y))
		self.sc = wx.SpinCtrl(panel, -1, '',  (x+100, y-4))
		self.sc.SetRange(0,10)
		#print " Value ", audioDeviceId
		self.sc.SetValue(audioDeviceId)
		y=y+65
		
		wx.StaticLine(panel, -1, pos=(x,y), size=wx.Size(560,7), style=wx.LI_HORIZONTAL)
		y=y+10
	
		wx.StaticText(panel, -1, 'Now Press Record button to record for few seconds & then Play. \n If you unable to hear your voice then change Sound Card & test again.)', (x,y))
		y=y+60

		
		self.button1 = wx.BitmapButton(panel, -1, wx.Image("icons/media-record.png", wx.BITMAP_TYPE_ANY).ConvertToBitmap())
		# ,style = wx.NO_BORDER)
		self.button1.SetPosition((x+50, y))
		self.button1.SetToolTip(wx.ToolTip("Start Recording"))
		self.Bind(wx.EVT_BUTTON, self.OnRecord, self.button1)
		self.button2 = wx.BitmapButton(panel, -1, wx.Image("icons/media-playback-start.png", wx.BITMAP_TYPE_ANY).ConvertToBitmap())
		# ,style = wx.NO_BORDER)
		self.button2.SetPosition((x+120, y))
		self.button2.SetToolTip(wx.ToolTip("Play"))
		self.Bind(wx.EVT_BUTTON, self.OnPlay, self.button2)
		self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)
		self.button2.Disable()

		self.button3 = wx.BitmapButton(panel, -1, wx.Image("icons/media-playback-stop.png", wx.BITMAP_TYPE_ANY).ConvertToBitmap())
		# ,style = wx.NO_BORDER)
		self.button3.SetPosition((x+190, y))
		self.button3.SetToolTip(wx.ToolTip("Stop Recording"))
		self.Bind(wx.EVT_BUTTON, self.OnStop, self.button3)
		self.button3.Disable()
	
		self.Bind(wx.EVT_SPINCTRL, self.OnSpin, self.sc)


	def OnSpin(self, event):
		global audioDeviceId
		audioDeviceId = self.sc.GetValue()
		#print "Setting Value ", audioDeviceId

	def OnRecord(self, event):
		self.button1.Disable()
		self.button3.Enable()
		self.button1.SetSize(self.button1.GetBestSize())
		self.statusBar.SetStatusText("Recording.... Please speak in microphone for few second and then Click on Play ?")
		pgsar.record(audioDeviceId, "/tmp/test.ogg")

	
	def OnStop(self, event):
		self.button1.SetSize(self.button1.GetBestSize())
		self.statusBar.SetStatusText("Saving Audio...")
		pgsar.save()
		self.statusBar.SetStatusText("Saved Audio")
		self.button3.Disable()
		self.button2.Enable()
	
	def OnPlay(self, event):
		pgsar.play("/tmp/test.ogg")
		self.statusBar.SetStatusText("Playing.... Can you hear your voice ? If not then try changing the Card No.")
		self.button1.Enable()
		

	def OnCloseWindow(self, event):
		self.Destroy()


class MyFrame(wx.Frame):
	def __init__(self, parent, ID, title):
		wx.Frame.__init__(self, parent, ID, title, size=(1000,700))
		##wx.Frame.__init__(self, None, wx.ID_ANY, 'Full display size', pos=(0, 0), size=wx.DisplaySize())
		self.Center()
		#self.ShowFullScreen(not self.IsFullScreen(), style=wx.FULLSCREEN_NOBORDER^wx.FULLSCREEN_NOTOOLBAR)
		self.started= False
		
		
		self.CreateMenubar()
		self.statusBar = self.CreateStatusBar()
				
		self.panel1 = wx.Panel(self,-1, style=wx.SUNKEN_BORDER)
		self.panel3 = wx.Panel(self,-1, style=wx.SUNKEN_BORDER)
		self.panel3.parent = self
		#self.panel1.SetBackgroundColour("BLUE")
		#self.panel2.SetBackgroundColour("RED")
		self.panel3.SetBackgroundColour("YELLOW")


		#b1 = wx.Button(self.panel1, 0, ' Start Recording ')
		self.buttonRec = wx.BitmapButton(self.panel1, -1, wx.Image("icons/media-record.png", wx.BITMAP_TYPE_ANY).ConvertToBitmap(),style = wx.NO_BORDER)
		self.buttonRec.Bind(wx.EVT_BUTTON,self.OnStartPresentation)
		self.buttonRec.SetToolTipString("Start Recording")
		

		self.buttonPause = wx.BitmapButton(self.panel1, -1, wx.Image("icons/media-playback-pause.png", wx.BITMAP_TYPE_ANY).ConvertToBitmap(),style = wx.NO_BORDER)
		self.buttonPause.Bind(wx.EVT_BUTTON,self.OnPausePresentation)
		self.buttonPause.SetToolTipString("Pause Recording")

		self.buttonUnPause = wx.BitmapButton(self.panel1, -1, wx.Image("icons/media-playback-start.png", wx.BITMAP_TYPE_ANY).ConvertToBitmap(),style = wx.NO_BORDER)
		self.buttonUnPause.Bind(wx.EVT_BUTTON,self.OnUnPausePresentation)
		self.buttonUnPause.SetToolTipString("Resume Recording")
		self.buttonUnPause.Hide()
		
		self.buttonStop = wx.BitmapButton(self.panel1, -1, wx.Image("icons/media-playback-stop.png", wx.BITMAP_TYPE_ANY).ConvertToBitmap(),style = wx.NO_BORDER)
		self.buttonStop.Bind(wx.EVT_BUTTON,self.OnEndPresentation)
		self.buttonStop.SetToolTipString("Stop Recording")
		self.buttonStop.Hide()
		
		
		buttonHome = wx.BitmapButton(self.panel1, -1, wx.Image("icons/go-first.png", wx.BITMAP_TYPE_ANY).ConvertToBitmap(),style = wx.NO_BORDER)
		buttonHome.Bind(wx.EVT_BUTTON,self.OnClickHome)
		buttonHome.SetToolTipString("First Page")
		

		buttonBack = wx.BitmapButton(self.panel1, -1, wx.Image("icons/go-previous.png", wx.BITMAP_TYPE_ANY).ConvertToBitmap(),style = wx.NO_BORDER)
		buttonBack.Bind(wx.EVT_BUTTON, self.OnBackward)
		buttonBack.SetToolTipString("Previous Page")

		buttonNext = wx.BitmapButton(self.panel1, -1, wx.Image("icons/go-next.png", wx.BITMAP_TYPE_ANY).ConvertToBitmap(),style = wx.NO_BORDER)
		buttonNext.Bind(wx.EVT_BUTTON, self.OnForward)
		buttonNext.SetToolTipString("Next Page")

		buttonLast = wx.BitmapButton(self.panel1, -1, wx.Image("icons/go-last.png", wx.BITMAP_TYPE_ANY).ConvertToBitmap(),style = wx.NO_BORDER)
		buttonLast.Bind(wx.EVT_BUTTON, self.OnClickEnd)
		buttonLast.SetToolTipString("Last Page")
		
		
		buttonGroup = wx.GridBagSizer(1, 8)
		
		buttonGroup.Add(self.buttonRec, (0,0), (1,1), wx.EXPAND)
		buttonGroup.Add(self.buttonStop, (0,1), (1,1), wx.EXPAND)
		buttonGroup.Add(self.buttonPause, (0,2), (1,1), wx.EXPAND)
		buttonGroup.Add(self.buttonUnPause, (0,3), (1,1), wx.EXPAND)
		buttonGroup.Add(buttonHome, (0,4), (1,1), wx.EXPAND)
		buttonGroup.Add(buttonBack, (0,5), (1,1), wx.EXPAND)
		buttonGroup.Add(buttonNext, (0,6), (1,1), wx.EXPAND)
		buttonGroup.Add(buttonLast, (0,7), (1,1), wx.EXPAND)
				
		self.SetAutoLayout(True)
		self.SetSizer(buttonGroup)
		self.Layout()
		
		self.timer = PythonTimer.TickTockTimer()
		#Start Timer when you click Start and not just load PDF

		box = wx.BoxSizer(wx.VERTICAL)
		box.Add(self.panel3, 10, wx.EXPAND)
		box.Add(self.panel1, 0, wx.EXPAND)
		self.SetAutoLayout(True)
		self.SetSizer(box)
		self.Layout()
		
		self.Bind(wx.EVT_KEY_DOWN, self.OnKeyboardKeyPress)
		self.panel3.Bind(wx.EVT_RIGHT_DOWN, self.CreateRightClickMenu)
		

	def OnAbout(self, event):
		dlg = EduVidAbout(self)
		dlg.ShowModal()
		dlg.Destroy()
		
	def OpenPreferencesMenu(self, event):
		dlg = PreferencesDialog(self, -1 , "Preferences")
		dlg.Show()
		dlg.Center()

	def OpenVideoFrame(self, event):
		f = WxWebcamTest.WxWebCamTest(self, -1 , "Video Test")
		f.Centre()
		f.Show(True)

	def OnForward(self,event):
		self.loadwindow.OnAction(event,"forward")
		if self.started == True:
			Curr_Page = self.loadwindow.GetCurrentPageNumber()
			self.TimeXMLdoc.InsertMostBasicClickNode(self.timer.GetTime(),Curr_Page)

	def OnBackward(self,event):
		self.loadwindow.OnAction(event,"backward")
		if self.started == True:
			Curr_Page = self.loadwindow.GetCurrentPageNumber()
			self.TimeXMLdoc.InsertMostBasicClickNode(self.timer.GetTime(),Curr_Page)

	def OnClickEnd(self,event):
		self.loadwindow.OnAction(event,"end")
		if self.started == True:
			Curr_Page = self.loadwindow.GetCurrentPageNumber()
			self.TimeXMLdoc.InsertMostBasicClickNode(self.timer.GetTime(),Curr_Page)

	def OnClickHome(self,event):
		self.loadwindow.OnAction(event,"home")
		if self.started == True:
			Curr_Page = self.loadwindow.GetCurrentPageNumber()
			self.TimeXMLdoc.InsertMostBasicClickNode(self.timer.GetTime(),Curr_Page)


	def OnOpenPDF(self,event):
		self.loadwindow = PDFwindow.PDFWindow(self.panel3)
		self.loadwindow.OnOpen(event)

	def OnOpenODP(self,event):
		self.loadwindow = ODPwindow.ODPWindow(self.panel3)
		self.loadwindow.OnOpen(event)


	def OnStartPresentation(self,event):
		if self.started == False:
			self.statusBar.SetStatusText("Recording Started : Move Slides, Speak , and then click Save Presentation ")
			self.started= True
			self.timer.StartTimer()
			self.TimeXMLdoc = TimeXML.TimeXML()
			self.TimeXMLdoc.InsertMostBasicClickNode(0,0)
			pgsar.record(0, "SpeakerAudio.ogg")
			
			self.buttonRec.Hide()
			self.buttonStop.Show()
			
			

	def OnPausePresentation(self,event):
		if self.started == True:
			self.statusBar.SetStatusText("Recording Paused")
			self.timer.Pause()
			pgsar.pause()
			
			self.buttonPause.Hide()
			self.buttonUnPause.Show()

	def OnUnPausePresentation(self,event):
		if self.started == True:
			self.statusBar.SetStatusText("Recording Started : Move Slides, Speak , and then click Save Presentation ")
			self.timer.UnPause()
			pgsar.resume()
			
			
			self.buttonPause.Show()
			self.buttonUnPause.Hide()

			
	def ToggelFullScreen(self,event):
		self.ShowFullScreen(not self.IsFullScreen(), style=wx.FULLSCREEN_NOBORDER^wx.FULLSCREEN_NOTOOLBAR)

	def OnEndPresentation(self,event):
		if self.started == True:
			self.statusBar.SetStatusText("Saving Your Timings")
			self.started = False
			self.TimeXMLdoc.SaveXML("time.xml")
			self.statusBar.SetStatusText("Saving Your Audio ")
			pgsar.save()
			self.statusBar.SetStatusText("Now Saving your presentation in Eduvid format")
			os.system("./GenerateEduvid.sh")
			self.statusBar.SetStatusText("Done - generated Eduvid 'output.eduvid'")
			os.system("./ConvertEduvidToHTML5.sh")
			self.statusBar.SetStatusText("Done - generated HTML5 version open './newoutput/index.html' in Firefox")
			
			self.buttonRec.Show()
			self.buttonStop.Hide()

			
	def OnKeyboardKeyPress(self,event):
		keycode = event.GetKeyCode() 
		print keycode
		if keycode == wx.WXK_UP:
			self.OnBackward(event)
		elif keycode == wx.WXK_DOWN:
			self.OnForward(event)
		elif keycode == wx.WXK_RIGHT:
			self.OnForward(event)
		elif keycode == wx.WXK_LEFT:
			self.OnBackward(event)
		elif keycode == wx.WXK_HOME:
			self.OnClickHome(event)
		elif keycode == wx.WXK_END:
			self.OnClickEnd(event)
			
	def OnClose(self, event):
		dlg = wx.MessageDialog(self,"Do you really want to close this application?","Confirm Exit", wx.CANCEL|wx.OK|wx.ICON_QUESTION)
		result = dlg.ShowModal()
		dlg.Destroy()
		if result == wx.ID_OK:
			os.system("rm -rf /tmp/odpviewer")
			self.Destroy()

	def CreateMenubar(self):
		menuBar = wx.MenuBar()
		self.SetMenuBar(menuBar)
		
		menuFile = wx.Menu()
		menuEdit = wx.Menu()
		menuView = wx.Menu()
		menuAbout = wx.Menu()
		
		fileOpenMenuItem1 = wx.MenuItem(menuFile, -1, '&Open PDF file\tCtrl+O', 'Select a PDF')
		fileOpenMenuItem1.SetBitmap(wx.Bitmap("icons/document-open.png"))
		
		
		#, wx.BITMAP_TYPE_PNG).ConvertToBitmap())
		fileOpenMenuItem2 = wx.MenuItem(menuFile,-1, '&Open ODP file', 'Select a Presentation')
		fileOpenMenuItem2.SetBitmap(wx.Image("icons/document-open.png", wx.BITMAP_TYPE_PNG).ConvertToBitmap())
		
		
	
		exitMenuItem = wx.MenuItem(menuFile,-1, '&Quit\tCtrl+Q', 'Exit the viewer')
		exitMenuItem.SetBitmap(wx.Image("icons/exit.png", wx.BITMAP_TYPE_PNG).ConvertToBitmap())
		
		
		menuViewFullScreen = menuView.Append(-1, "Full Screen\tF11", "Full Screen", wx.ITEM_CHECK)

		aboutMenuItem = wx.MenuItem(menuAbout, -1, '&About EduVid', 'About EduVid Recorder')
		aboutMenuItem.SetBitmap(wx.Image("icons/exit.png", wx.BITMAP_TYPE_PNG).ConvertToBitmap())
		
		
		PreferencesMenuItem = wx.MenuItem(menuEdit, -1,'&Preferences\tCtrl+P', 'View Prefrences. Still not configured.')
		PreferencesMenuItem.SetBitmap(wx.Image("icons/preferences-desktop.png", wx.BITMAP_TYPE_PNG).ConvertToBitmap())
		
		OpenVideoFrameMenuItem = wx.MenuItem(menuEdit,-1, 'Video Test', 'View Prefrences. Still not configured.')
		OpenVideoFrameMenuItem.SetBitmap(wx.Image("icons/preferences-desktop.png", wx.BITMAP_TYPE_PNG).ConvertToBitmap())
		
		
		menuBar.Append(menuFile, '&File')
		menuBar.Append(menuEdit, '&Edit')
		menuBar.Append(menuView, '&View')
		menuBar.Append(menuAbout, '&About')
		
		menuFile.AppendItem(fileOpenMenuItem1)
		menuFile.AppendItem(fileOpenMenuItem2)
		menuFile.AppendSeparator()
		menuFile.AppendItem(exitMenuItem)
		menuAbout.AppendItem(aboutMenuItem)
		menuEdit.AppendItem(PreferencesMenuItem)
		menuEdit.AppendItem(OpenVideoFrameMenuItem)
		
		self.Bind(wx.EVT_MENU, self.OnOpenPDF, fileOpenMenuItem1)
		self.Bind(wx.EVT_MENU, self.OnOpenODP, fileOpenMenuItem2)
		self.Bind(wx.EVT_MENU, self.OnClose, exitMenuItem)
		self.Bind(wx.EVT_MENU, self.OnAbout, aboutMenuItem)
		self.Bind(wx.EVT_MENU, self.OpenPreferencesMenu, PreferencesMenuItem)
		self.Bind(wx.EVT_MENU, self.OpenVideoFrame, OpenVideoFrameMenuItem)
		self.Bind(wx.EVT_MENU, self.ToggelFullScreen, menuViewFullScreen)
	
	def CreateRightClickMenu(self,event):
		
		menu = wx.Menu()
		minimize = wx.MenuItem(menu, wx.NewId(), 'Minimize')
		menu.AppendItem(minimize)
		
		close = wx.MenuItem(menu, wx.NewId(), 'Close')
		menu.AppendItem(close)
		
		self.PopupMenu(menu, event.GetPosition())


#if __name__=="__main__":
app = wx.PySimpleApp()
frame = MyFrame(None, -1, "Eduvid Slidecasting Recorder")
frame.Show()
app.MainLoop()
