#!/usr/bin/env python
# coding: utf-8
""" 
    wxPDFViewer - Simple PDF Viewer using Python-Poppler and wxPython 
    http://www.roboture.in - sheel.loverboy@gmail.com
"""
import wx
import wx.lib.wxcairo as wxcairo
#import sys
import os
import poppler
import PDFwindow
import time
import PythonTimer
import TimeXML



class MyFrame(wx.Frame):
     def __init__(self, parent, ID, title):
        wx.Frame.__init__(self, parent, ID, title)
        
        "Create a menu bar with Open, Exit items"
        menuBar = wx.MenuBar()
        # Tell our Frame about this MenuBar
        self.SetMenuBar(menuBar)
        menuFile = wx.Menu()
	menuEdit = wx.Menu()
        menuBar.Append(menuFile, '&File')
        menuBar.Append(menuEdit, '&Edit')
        # NOTE on wx ids - they're used everywhere, we don't care about them
        # Used to handle events and other things
        # An id can be -1 or wx.ID_ANY, wx.NewId(), your own id
        # Get the id using object.GetId()
        
        panel3 = wx.Panel(self,-1, style=wx.SUNKEN_BORDER)
        
        self.pdfwindow1 = PDFwindow.PDFWindow(panel3)
        fileOpenMenuItem = menuFile.Append(-1, '&Open PDF file', 'Select a PDF')
        self.Bind(wx.EVT_MENU, self.pdfwindow1.OnOpen, fileOpenMenuItem)
        exitMenuItem = menuFile.Append(-1, 'Exit', 'Exit the viewer')        
        self.Bind(wx.EVT_MENU, self.pdfwindow1.OnClose, exitMenuItem)
        exitMenuItem2 = menuFile.Append(-1, 'Print', 'To print the page')        
        exitMenuItem3 = menuEdit.Append(-1, 'Preferences', 'Exit the viewer')                           

        panel1 = wx.Panel(self,-1, style=wx.SUNKEN_BORDER)
        panel2 = wx.Panel(self,-1, style=wx.SUNKEN_BORDER)
        
        panel1.SetBackgroundColour("BLUE")
        panel2.SetBackgroundColour("RED")

        
        b1 = wx.Button(panel1, 0, ' Button 1 ')
        b2 = wx.Button(panel1, 0, ' Button 2 ')
        b3 = wx.Button(panel1, 0, ' Button 3 ')
        b4 = wx.Button(panel1, 0, ' Button 4 ')
        #b4 = wx.Button(panel1, 0, ' Button 4 ', size=bs)
        #but = wx.BoxSizer(wx.VERTICAL)
        #vb = wx.BoxSizer(wx.VERTICAL)
        but = wx.GridBagSizer(1, 4)
        #but.Add(b1, 0, wx.EXPAND)
        #but.Add(b1, (1,1),(2,2), wx.EXPAND)
        but.Add(b1, (0,0), (1,1), wx.EXPAND)
        but.Add(b2, (0,1), (1,1), wx.EXPAND)
        but.Add(b3, (0,2), (1,1), wx.EXPAND)
        but.Add(b4, (0,3), (1,1), wx.EXPAND)
        self.SetAutoLayout(True) 
        self.SetSizer(but)
        self.Layout()
        
        self.pdfwindow = PDFwindow.PDFWindow(panel3)
        
        button5 = wx.Button(panel2,0,"Open")#,(80,550))
        button5.Bind(wx.EVT_BUTTON, self.OnOpen)

        button2 = wx.Button(panel2,0,"Forward")#,(230,550))
        button2.Bind(wx.EVT_BUTTON, self.OnForward)

        button3 = wx.Button(panel2,0,"Back")#,(380,550))
        button3.Bind(wx.EVT_BUTTON, self.OnBackward)    

        button1 = wx.Button(panel2,0,"Home")#,(80,600))
        button1.Bind(wx.EVT_BUTTON,self.pdfwindow.OnClickHome)

        button4 = wx.Button(panel2,0,"Save")#,(230,600))
        button4.Bind(wx.EVT_BUTTON,self.OnSave)

        button6 = wx.Button(panel2,0,"Close")#,(380,600))
        button6.Bind(wx.EVT_BUTTON, self.pdfwindow.OnClose)

        self.statusBar = self.CreateStatusBar()
        
        bu = wx.GridBagSizer(1, 6)
                
        bu.Add(button1, (0,0), (1,1), wx.EXPAND)
        bu.Add(button2, (0,1), (1,1), wx.EXPAND)
        bu.Add(button3, (0,2), (1,1), wx.EXPAND)
        bu.Add(button4, (0,3), (1,1), wx.EXPAND)
        bu.Add(button5, (0,4), (1,1), wx.EXPAND)
        bu.Add(button6, (0,5), (1,1), wx.EXPAND)
       
       
        self.SetAutoLayout(True) 
        self.SetSizer(bu)
        self.Layout()

        box = wx.BoxSizer(wx.VERTICAL)
        box.Add(panel3, 10, wx.EXPAND)
        box.Add(panel1, 2, wx.EXPAND)
        box.Add(panel2, 3, wx.EXPAND)
        self.SetAutoLayout(True)
        self.SetSizer(box)
        self.Layout()
        
        
        self.timer = PythonTimer.TickTockTimer()
	
	#Start Timer when you click Start and not just load PDF
	self.TimeXMLdoc = TimeXML.TimeXML()

     def OnForward(self,event):
        self.pdfwindow.OnForward(event)
        Curr_Page = self.pdfwindow.GetCurrentPageNumber()
	self.TimeXMLdoc.InsertMostBasicClickNode(self.timer.GetTime(),Curr_Page)

     def OnBackward(self,event):
        self.pdfwindow.OnBackward(event)
        Curr_Page = self.pdfwindow.GetCurrentPageNumber()
	self.TimeXMLdoc.InsertMostBasicClickNode(self.timer.GetTime(),Curr_Page)
        
     def OnOpen(self,event):
        self.pdfwindow.OnOpen(event)
        self.timer.StartTimer()
        self.TimeXMLdoc.InsertMostBasicClickNode(0,0)
        
     def OnSave(self,event):
        self.TimeXMLdoc.SaveXML("time.xml")
        
        
#if __name__=="__main__":
app = wx.PySimpleApp()
frame = MyFrame(None, -1, "Sizer Test")
frame.Show()
app.MainLoop()

