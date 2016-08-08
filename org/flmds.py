#!/usr/bin/python

class fmd:
	'This class manages file modes'
	__filemodes = ("r", "rb", "r+", "rb+", "w", "wb", "w+", "wb+", "a", "ab", "a+", "ab+");
	__filemode = "";
	
	def __init__(self, mdi=0):
		self.__filemode = self.__filemodes[mdi]
		
	def setmd(self, mdi):
		if(mdi < 0 & mdi >= len(self.__filemodes)):
			mdi = 0;
		self.__filemode = self.__filemodes[mdi];
	def getmd(self):
		return self.__filemode;
		
	def modes(self):
		for index in range(len(self.__filemodes)):
			print "---> %d : %s" % (index, self.__filemodes[index]);