#!/usr/bin/python

import re


class Ipsconv:

    __header = ""

    def __init__(self, filein, fileout):
        self.__filein = filein
        self.__fileout = fileout

    def setfilein(self, filein):
        self.__filein = filein

    def setfileout(self, fileout):
        self.__fileout = fileout

    def getfilein(self):
        return self.__filein

    def getfileout(self):
        return self.__fileout

    def getheader(self):
        # set pointer to the start
        if self.__filein.tell() != 0:
            self.__filein.seek(0, 0)
        # start read line by line end return header
        for line in self.__filein:
            l = line[0:-1].rstrip()
            if l != "":
                if not self.__isip(l):
                    return l

    def __isip(self, line):
        if re.match(r'(^(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})*)', line, re.I):
           return True
        else:
           return False

    def convert(self):
        if self.__filein.tell() != 0:
            self.__filein.seek(0, 0)  # set pointer to the start
        # start read line by line
        for line in self.__filein:
            l = line[0:-1].rstrip()
            if l != "":
                if self.__isip(l):
                    if re.match(r'(^(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})/\d{1,2}$)', l, re.I):
                        ips = self.__getrange(l, 1)
                        for each in ips:
                            ip = '%s\n' % each
                            self.__fileout.write(ip)

                    if re.match(r'(^(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})([\s]*-[\s]*)(\d{1,3}$))', l, re.I):
                        ips = self.__getrange(l, 2)
                        for each in ips:
                            ip = '%s\n' % each
                            self.__fileout.write(ip)

                    if re.match(r'(^(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})'
                                r'([\s]*-[\s]*)'
                                r'(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3}))', l, re.I):
                        ips = self.__getrange(l, 3)
                        for each in ips:
                            ip = '%s\n' % each
                            self.__fileout.write(ip)

    def __getrange(self, ipblock, mode):

        i = 1
        ips = []

        if mode == 1:
            ips.append(ipblock[0:ipblock.find('/')])
            ipaddress = ipblock[0:ipblock.find('/')]
            ipcomp = self.__splitip(ipaddress)
            hosts = 2 ** (32 - int(ipblock[ipblock.find('/')+1:]))

            while i < hosts:
                ipcomp[3] += 1
                if ipcomp[3] == 255:
                    ipcomp[2] += 1
                    if ipcomp[2] == 255:
                        ipcomp[1] += 1
                        if ipcomp[1] == 255:
                            ipcomp[0] += 1
                ip = '%d.%d.%d.%d' % (ipcomp[0], ipcomp[1], ipcomp[2], ipcomp[3])
                ips.append(ip)
                i += 1
        elif mode == 2:
            ipcomponents = ipblock.split('-')
            if " " in ipcomponents[0]:
                ipcomponents[0].replace(" ", "")
            if " " in ipcomponents[1]:
                ipcomponents[1].replace(" ", "")
            ipcomp = self.__splitip(ipcomponents[0])
            ips.append(ipcomponents[0])
            hosts = int(ipcomponents[1])
            while i <= hosts:
                ipcomp[3] += 1
                ip = '%d.%d.%d.%d' % (ipcomp[0], ipcomp[1], ipcomp[2], ipcomp[3])
                ips.append(ip)
                i += 1

        elif mode == 3:
            ipcomponents = ipblock.split('-')
            ipleft = self.__splitip(ipcomponents[0])
            ipright = self.__splitip(ipcomponents[1])
            ips.append(ipcomponents[0])
            hosts = (((ipright[0] - ipleft[0]) * 256 ** 3) + ((ipright[1] - ipleft[1]) * 256 ** 2) +
                     ((ipright[2] - ipleft[2]) * 256) + (ipright[3] - ipleft[3]))
            while i <= hosts:
                ipleft[3] += 1
                if ipleft[3] == 255:
                    ipleft[2] += 1
                    if ipleft[2] == 255:
                        ipleft[1] += 1
                        if ipleft[1] == 255:
                            ipleft[0] += 1
                ip = '%d.%d.%d.%d' % (ipleft[0], ipleft[1], ipleft[2], ipleft[3])
                ips.append(ip)
                i += 1

        return ips

    def __splitip(self, ip):
        if " " in ip:
            ip.replace(" ", "")
        comp = ip.split('.')
        ipcomp = []
        for x in comp:
            ipcomp.append(int(x))
        return ipcomp
