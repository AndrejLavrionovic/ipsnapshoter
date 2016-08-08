#!/usr/bin/python

import os
import os.path
import flmds

class fl:
	'This us parent class for other classes that will work with files'
	
	__filename = "";
	__filepath = "";
	__filemode = "";
	
	def __init__(self, f="file.txt", m=0):
		self.__md = flmds.fmd(m);
		self.__filename = f;
		self.__filemode = self.__md.getmd();
	
	def setfn(self, fn):
		self.__filename = fn
	def getfn(self):
		return self.__filename
	def setfp(self, fp):
		self.__filepath = fp
	def getfp(self):
		return self.__filepath
	def setfm(self, md):
		self.__md.setmd(md);
		self.__filemode = self.__md.getmd();
	def getfm(self):
		return self.__filemode;
