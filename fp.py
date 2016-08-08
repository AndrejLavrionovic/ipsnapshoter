#!/usr/bin/python

import os
import os.path

class fp:
	__root = ""
	__files = ""
	
	def __init__(self):
		self.__root = os.getcwd();
		self.__files = self.__root + "/files";
		
	def getfp(self):
		return self.__files

        def getcp(self):
                return self.__root
	
	def getps(self):
		print self.__root;
		print self.__files;
		
ps = fp();
ps.getps();
