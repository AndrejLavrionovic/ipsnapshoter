#!/usr/bin/python

import re

class ipp:
    'Appending port (-s) to given ip address'

    __ipps = []
    __deftcpports = ("80", "2080", "5060", "5120", "5550", "7080", "8080", "8081", "9080", "9090", "9999", "443")
    __ports = []

    def __init__(self, ip='0.0.0.0', ports=[], mode=1):
        self.__ip=ip
        self.__mode=mode
        if(len(ports)==0):
            self.__ports = list(self.__deftcpports)
        else:
            self.__ports = ports

    def setm(self, m):
        self.__mode=m
    def getm(self):
        return self.__mode
    def setip(self, ip):
        self.__ip=ip
    def getip(self):
        return self.__ip
    def setports(self, ports):
        self.__ports = ports
    def getports(self):
        return self.__ports
    def getpn(self):
        return len(self.__ports)

    def getipp(self):
        #reset __ipps
        if(len(self.__ipps)>0):
            self.__ipps[:]=[]
        if(self.__mode == 1):
            if(self.isip(self.__ip)):
                for each in self.__ports:
                    ip = self.__ip+':'+each
                    self.__ipps.append(ip)
            else:
                print "IP address is not valid"
        return self.__ipps

    def isip(self, ip):
        searchObj = re.match(r'^(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})$', ip, re.M|re.I)
        if searchObj:
            grps = searchObj.groups()
            for g in grps:
                if(int(g) > 255):
                    return False
            return True
        else:
            print "not an IP"
            return False
