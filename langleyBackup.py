#!/usr/bin/env python

import subprocess
import os
import sys

PATH = os.path.dirname(os.path.realpath(sys.argv[0]))

class LangleyBackup():
	def __init__(self):
		if not os.path.exists('/mnt/usb1/'):
        		os.makedirs('/mnt/usb1/')

		subprocess.call("sudo mount /dev/sda1 /mnt/usb1 > /dev/null 2>&1", shell=True)
		self.megaUsername = None
		self.getLocalDirectoryList()
		self.getRemoteDirectoryList()

	def getMegaCredentials(self):
		lines = open(PATH+'/megaLogin.txt','r').read().split('\n')
		self.megaUsername = lines[0]
		self.megaPassword = lines[1]

	def ignoreDirectory(self,dir):
		if dir.find('/.') != -1:
			return True
		elif dir.find('System Volume Information') != -1:
			return True

		return False

	def getLocalDirectoryList(self):
		statvfs = os.statvfs('/mnt/usb1/')
		f = open(PATH+'/fileList.txt', 'w')
		f.write(str(statvfs.f_frsize * statvfs.f_bfree)+'\n')
		f.close()
		f = open(PATH+'/fileList.txt', 'a')
		for x in os.walk('/mnt/usb1'):
			if not self.ignoreDirectory(x[0]):
                                f.write(x[0]+'\n')

		f.close()

	def getRemoteDirectoryList(self):
		if self.megaUsername == None:
			self.getMegaCredentials()

		subprocess.call(['megals', '-u', self.megaUsername, '-p', self.megaPassword])

backup = LangleyBackup()
