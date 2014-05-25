#!/usr/bin/env python

# This is the MIT license:
# http://www.opensource.org/licenses/mit-license.php

# Copyright (c) 2009 Digital Achievement Incorporated and contributors.
# Copyright (c) 2011 Narendra Sisodiya, ELPA Technologies, http://narendrasisodiya.com


# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:

# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


import dbus
import gst
import sys
import time

class PythonGstreamerAudioRecorder:

	def list_capture_devices(self):
		bus = dbus.SystemBus()
		hal_manager = bus.get_object("org.freedesktop.Hal", "/org/freedesktop/Hal/Manager")
		hal_manager = dbus.Interface(hal_manager, "org.freedesktop.Hal.Manager")

		devices = hal_manager.FindDeviceStringMatch("alsa.type", "capture")

		identifiers = []

		for dev in devices:
			device = bus.get_object("org.freedesktop.Hal", dev)

			card = device.GetAllProperties(dbus_interface="org.freedesktop.Hal.Device")
			if card["alsa.card"] not in identifiers:
				print "%d. %s" % (card["alsa.card"], card["alsa.card_id"])
				identifiers.append(card["alsa.card"])

		return identifiers

	def get_capture_device_id(self):

		capture_device_id = None

		while capture_device_id == None:
			identifiers = self.list_capture_devices()
			print "Enter a capture device ID: "
			line = sys.stdin.readline().strip()
		
			try:
				capture_device_id = int(line)
		
				if capture_device_id in identifiers:
					return capture_device_id
			except ValueError:
				print "value error"


			print "Invalid entry\n"
			capture_device_id = None
	
	def pause(self):
		print "Paused"
		self.pipeline.set_state(gst.STATE_PAUSED)
	
	def resume(self):
		print "Resumed"
		self.pipeline.set_state(gst.STATE_PLAYING)
			
	def record(self, device_id, capture_path):
		self.pipeline = gst.parse_launch("""alsasrc device=hw:%d ! audioconvert ! level name=recordlevel interval=10000000 ! audioconvert ! vorbisenc ! oggmux ! filesink location=%s""" % (device_id, capture_path))
		''' audioconvert ! rawvorbisenc ! oggmux ! filesink'''
		''' audioconvert ! flacenc ! filesink'''
		
		
		self.pipeline.set_state(gst.STATE_PLAYING)

		#print "Recording, press Save to stop"
		#sys.stdin.readline()

		#self.pipeline.set_state(gst.STATE_NULL)
		#time.sleep(5)
	
	def play(self, name):
		self.f = name
		#self.pipeline = gst.parse_launch("""playbin uri=file:///home/narendra/MyData/MyWork/Python/wxpdfviewer/test3.ogg""")
		self.pipeline = gst.parse_launch("""playbin uri=file://%s""" % (self.f))
		self.pipeline.set_state(gst.STATE_PLAYING)
		print "playing, press enter to stop"
		#sys.stdin.readline()
		#self.pipeline.set_state(gst.STATE_NULL)
		#time.sleep(5)

	def save(self):
		self.pipeline.set_state(gst.STATE_NULL)
		time.sleep(3)
		
	def stop(self):
		self.pipeline.set_state(gst.STATE_NULL)
		time.sleep(2)
		
'''	

if __name__ == "__main__":
	oparser = optparse.OptionParser()
	oparser.add_option("-f", "--file", dest="path",
					 help="save to FILE", metavar="FILE")
	oparser.add_option("-d", "--device", dest="device",
					 help="Use device DEVICE", metavar="DEVICE")
	(options, args) = oparser.parse_args()


	device_id = options.device
	capture_path = options.path
	
	audiorecorder = PythonGstreamerAudioRecorder()
	
	if device_id is None:
		device_id = audiorecorder.get_capture_device_id()

	if capture_path is None:
		capture_path = get_capture_path()

	#audiorecorder.play()
	audiorecorder.record(device_id, capture_path)


'''

'''
import PythonGstreamerAudioRecorder
>>> audiorecorder = PythonGstreamerAudioRecorder.PythonGstreamerAudioRecorder()
>>> device_id = audiorecorder.get_capture_device_id()
2. HSPADataCard HSPADataCard
0. HDA Intel
Enter a capture device ID: 0

>>> capture_path = "test1.ogg"





'''

