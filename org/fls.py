#!/usr/bin/python

import fc


class f:
    """Instances of source and output files"""

    def __init__(self, infile="ips.txt", outfile="out.txt", nmapout="out.xml"):
        self.__infile = fc.fl(infile)
        self.__outfile = fc.fl(outfile)
        self.__nmapout = fc.fl(nmapout)

    def setfin(self, infile):
        self.__infile = infile

    def setfout(self, outfile):
        self.__outfile = outfile

    def setfnmap(self, nmapout):
        self.__nmapout = nmapout

    def getfin(self):
        return self.__infile.getfn()

    def getfout(self):
        return self.__outfile.getfn()

    def getfnmap(self):
            return self.__nmapout.getfn()

    def setinm(self, m):
        self.__infile.setfm(m)

    def setoutm(self, m):
        self.__outfile.setfm(m)

    def setnmapm(self, m):
        self.__nmapout.setfm(m)

    def getinm(self):
        return self.__infile.getfm()

    def getoutm(self):
        return self.__outfile.getfm()

    def getnmapm(self):
        return self.__nmapout.getfm()
