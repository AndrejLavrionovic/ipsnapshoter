#!/usr/bin/python

import argparse
import sys
from org.foutput import *


# Create cli parce
def create_cli_parser():
    parser = argparse.ArgumentParser(description="AltechScanner is a tool that\
    scann ip addresses and capture its screenshots")
    parser.add_argument('-p', default=None, help='list of ports separated by \',\'\
    with no white spaces. Ports include numbers only.')
    parser.add_argument('-f', default=None, help='Output file contain all ip addresses.\
    With no -p specified will run through all ips with bunch of default ports. If ports are specified\
    utility will run through all ip addresses with a bunch of specified ports.')
    parser.add_argument('-n', default=None, help='input File that contain list of ips blocks (CIDRs)\
    that will be converted into ips.txt and report file will be named as a header in the file.')
    args = parser.parse_args()
    if args.p is not None:
        if ',' in args.p:
            args.p = args.p.split(',')
            for item in args.p:
                if '-' in item:
                    s, e = item.split('-')
                    start = int(s)
                    end = int(e)
                    args.p.remove(item)
                    if start < end:
                        while start <= end:
                            args.p.append(str(start))
                            start += 1
                    else:
                        print '[-->] Error: range must begin from smoller to higher number'
                        sys.exit()
        else:
            args.p = [args.p]
        print args.p
    return args
    

def runscanner(cliparsed, ips_bunch=500):
    print '==> scan source file and convert it into outfile'
    fo = fout()
    if cli_parsed.n is not None:
        fo.runipconverter(cliparsed.n)
    if cli_parsed.f is not None:
        fo.runfileconverter(cliparsed.p, cliparsed.f)
    else:
        fo.runnmapconverter()


if __name__ == "__main__":
    cli_parsed = create_cli_parser()
    runscanner(cli_parsed)

# Testing
fls = f()
print fls.getfin() + " > " + fls.getinm() + "\n" + fls.getfout() + " > " + fls.getoutm()
ps = fp.fp()
ps.getps()
