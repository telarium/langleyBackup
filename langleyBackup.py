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
		self.fileIgnoreList = None
		self.doBackup()

	def getMegaCredentials(self):
		print "Logging into Mega Upload..."
		lines = open(PATH+'/.megaLogin','r').read().split('\n')
		self.megaUsername = lines[0].rstrip()
		self.megaPassword = lines[1].rstrip()

	def ignoreFile(self,fileName):
		if self.fileIgnoreList == None:
			self.fileIgnoreList = []
			f = open(PATH+'/fileIgnoreList.txt', 'r')
                        files = f.read().split('\n')
			f.close()
                        for file in files:
				if file[:1] != '#' and file != "":
					self.fileIgnoreList.append(file)

		if fileName == '' or fileName == ' ' or fileName.find('/.') != -1:
			return True
		else:
			for ignoreName in self.fileIgnoreList:
				if fileName.find(ignoreName) != -1:
					return True

		return False

	def getLocalDirectoryList(self):
		self.ignoreFile("BS Show")
		statvfs = os.statvfs('/mnt/usb1/')
		blocks = statvfs.f_frsize * statvfs.f_bfree
		label = subprocess.check_output(['sudo','blkid','-o','value','-s','LABEL','/dev/sda1']).rstrip()
		try:
			f = open(PATH+'/fileList.txt', 'r')
			fileInfo = f.read().split('\n')
			f.close()
			if int(fileInfo[0].rstrip()) == blocks and fileInfo[1].rstrip() == label:
				print "File log not updated."
				return
		except:
			f = None

		f = open(PATH+'/fileList.txt', 'w')
		f.write(str(blocks)+'\n'+label+'\n')
		f.close()
		f = open(PATH+'/fileList.txt', 'a')
		dir = None
		print "Scanning file system..."
		for x in os.walk('/mnt/usb1'):
			dir = x[0]
			f.write(dir+'\n')

		f.close()

	def getRemoteDirectoryList(self):
		if self.megaUsername == None:
			self.getMegaCredentials()

		print "Fetching Mega Upload file list..."
		subprocess.call(['megals', '-u', self.megaUsername, '-p', self.megaPassword,'--reload'])

	def syncDirectory(self,dir):
		if self.ignoreFile(dir):
			return
		else:
			try:
				files = os.listdir(dir)
				remoteDir = dir.replace('mnt/usb1','Root')
				subprocess.call(['megamkdir', '-u', self.megaUsername, '-p', self.megaPassword, remoteDir, '--reload'],stdout=open(os.devnull, 'w'), stderr=subprocess.STDOUT)
				for file in files:
					fullPath = dir+'/'+file
					if not os.path.isdir(file) and not self.ignoreFile(fullPath):
						print 'Uploading: ' + remoteDir+'/'+file
						subprocess.call(['megaput', '-u', self.megaUsername, '-p', self.megaPassword, '--path', remoteDir+'/'+file, fullPath,'--reload','--disable-previews'],stdout=open(os.devnull, 'w'), stderr=subprocess.STDOUT)
			except Exception as msg:
				print msg
		
	def doBackup(self):
		self.getLocalDirectoryList()
                self.getRemoteDirectoryList()

		f = open(PATH+'/fileList.txt', 'r')
                directories = f.read().split('\n')
		del directories[0:2] # Ignore headers
                f.close()

                for dir in directories:
			self.syncDirectory(dir)
		

backup = LangleyBackup()
