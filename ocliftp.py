#!/usr/bin/python
"""
ocliftp - NON interactive FTP client
Copyright (C) 2014  Michal Orovan

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
"""

from ftplib import FTP
from os import path
from optparse import OptionParser

def saveChunk(c,f):
	f.write(c)

class MyFTP(FTP):
	def __init__(self,host):
		FTP.__init__(self,host)
	def download(self,remoteFilePath,localFilePath):
		newFile=open(localFilePath,'ab')
		ftp.retrbinary('RETR '+remoteFilePath,lambda x:saveChunk(x,newFile))
		newFile.close()
	def upload(self,localFilePath,remoteFilePath):
		localFile=open(localFilePath,'rb')
		ftp.storbinary('STOR '+remoteFilePath,localFile)
		localFile.close()

class Parser(OptionParser):
	def __init__(self,helpStr):
		OptionParser.__init__(self,helpStr)
		self.add_option('-u','--user',dest='user',type='string',default='anonymous',help='FTP username')
		self.add_option('-p','--password',dest='pas',type='string',default='',help='FTP password')
		self.add_option('-l','--local',dest='lfp',type='string',help='local file path')
		self.add_option('-r','--remote',dest='rfp',type='string',help='remote file path')
		self.add_option('-D','--download',dest='dl',action="store_true",help='download file')
		self.add_option('-U','--upload',dest='ul',action="store_true",help='download file')
		self.options,self.host=self.parse_args()
		if len(self.host)!=1:
			print(self.error('invalid host'))
			exit()
		if self.options.dl and self.options.ul:
			print(self.error('Can not uplaod and download simultaneously'))
			exit()			
		if self.options.lfp==None or self.options.rfp==None:
			print(self.error('Specify remote (-r) and local(-l) file paths'))
			exit()

parser=Parser('%prog [options] host')
try:
	ftp=MyFTP(parser.host[0])
except:
	print('# Can not establish connection')
	exit()
try:
	ftp.login(parser.options.user,parser.options.pas)
except:
	print('# Username or password is incorrent')
	exit()

if parser.options.dl:
	if path.isfile(parser.options.lfp):
		print("# File already exists.")
		exit()
	try:
		ftp.download(parser.options.rfp,parser.options.lfp)
	except:
		print('# Remote file cant be found.')
		exit()
elif parser.options.ul:
	if not path.isfile(parser.options.lfp):
		print("# Local file does not exist.")
		exit()
	ftp.upload(parser.options.lfp,parser.options.rfp)
print('# Finished successfuly')
