#!/usr/bin/env python

import subprocess
import os
import sys

PATH = os.path.dirname(os.path.realpath(sys.argv[0]))

class LangleyBackup():
	def __init__(self):
		if not os.path.exists('/mnt/usb1/'):
        		os.makedirs('/mnt/usb1/')

		subprocess.call('sudo mount /dev/sda1 /mnt/usb1 > /dev/null 2>&1', shell=True)
		subprocess.Popen('sudo /etc/init.d/samba restart', shell=True,stdout=open(os.devnull, 'w'), stderr=subprocess.STDOUT)
		self.megaUsername = None
		self.getLocalDirectoryList()
		self.getRemoteDirectoryList()

	def getMegaCredentials(self):
		print "Logging into Mega Upload..."
		lines = open(PATH+'/megaLogin.txt','r').read().split('\n')
		self.megaUsername = lines[0].rstrip()
		self.megaPassword = lines[1].rstrip()

	def ignoreDirectory(self,dir):
		if dir.find('/.') != -1:
			return True
		elif dir.find('System Volume Information') != -1:
			return True

		return False

	def getLocalDirectoryList(self):
		statvfs = os.statvfs('/mnt/usb1/')
		label = subprocess.check_output(['sudo','blkid','-o','value','-s','LABEL','/dev/sdb1']).rstrip()
		f = open(PATH+'/fileList.txt', 'w')
		f.write(str(statvfs.f_frsize * statvfs.f_bfree)+'\n'+label+'\n')
		f.close()
		f = open(PATH+'/fileList.txt', 'a')
		for x in os.walk('/mnt/usb1'):
			if not self.ignoreDirectory(x[0]):
                                f.write(x[0]+'\n')

		f.close()

	def getRemoteDirectoryList(self):
		if self.megaUsername == None:
			self.getMegaCredentials()

		print "Fetching Mega Upload file list..."
		subprocess.call(['megals', '-u', self.megaUsername, '-p', self.megaPassword])

backup = LangleyBackup()
