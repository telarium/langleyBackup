#!/usr/bin/env python

import subprocess
import os
import sys

class LangleyBackup():
	def __init__(self):
		subprocess.call("sudo mount /dev/sda1 /mnt/usb/ > /dev/null 2>&1", shell=True)
		self.getDirectoryList()
		print "oh hello!"

	def getDirectoryList(self):
		directories = []
		for root, subdirs, files in os.walk("/mnt/usb/"):
			directories.append(root)

		print directories

backup = LangleyBackup()
