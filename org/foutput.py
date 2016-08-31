import os
import os.path
import subprocess
import fp
import xml.etree.ElementTree as ET
from fls import *
from ipp import *
from time import strftime, gmtime
from ipsconverter import Ipsconv


class fout:

  # class instances
  __pathinstance = fp.fp()
  __fls = f('ips.txt')
  __resdirname = strftime('%Y%j%H%M%S', gmtime())
  
  def __init__(self, ips_bunch=500):
    self.__ips_bunch = ips_bunch

  # setters and getters
  def setipbunch(self, ips_bunch):
    self.__ips_bunch = ips_bunch
  def getipbunvh(self):
    return self.__ips_bunch

  def getpaths(self):
    print self.__pathinstance.getcp()
    print self.__pathinstance.getfp()

  # if -f flag is set up
  def runfileconverter(self, ports, filein):
    print 'convert file into output file'
    # Set components to open files
    if filein != "":
      self.__fls.setfin(filein)
    self.__fls.setinm(1)
    self.__fls.setoutm(7)

    # open source file
    inf = self.__opensourcefile()

    # Calculate ips and manage outfiles
    ipnumber = 0
    for line in inf:
      ipnumber += 1
    if ports is not None:
      p = ipp('0.0.0.0', ports)
    else:
      p = ipp()
    ipoutnumber = ipnumber * p.getpn()
    print '===> number of ips = %d' % (ipnumber)
    print '===> number of ports = %d' % (p.getpn())
    print '===> number of ips with ports = %d' % (ipoutnumber)

    self.__runscan(inf, ipoutnumber, ports, self.__ips_bunch)

    inf.close()

  # default mode with nmap converting
  def runnmapconverter(self):
    # 1) run nmap and
    # open source file and specify outfile
    inf = os.path.join(self.__pathinstance.getfp(), self.__fls.getfin())
    nmapout = os.path.join(self.__pathinstance.getfp(), self.__fls.getfnmap())
    nmaprun = 'nmap --top-ports 2000 -T4 -iL ' + inf + ' -oX ' + nmapout
    nmapscann = subprocess.Popen(nmaprun, shell=True)
    nmapscann.wait()
    # 2) parse nmap.xml into tree
    os.chdir(self.__pathinstance.getfp())
    tree = ET.parse(nmapout)  # parse xml file into tree
    root = tree.getroot()  # get root element
    # 3) create output file instance
    # 3.1) check how many ips
    counter = 0
    for host in root.iter('host'):
      ports = host.find('ports')  # searching for ports tag in host element
      for p in ports.iter('port'):  # searching for ports
        state = p.find('state').get('state')
        if state == 'open':
          counter += 1
    i = 0
    bunch = 1
    source=os.path.join(self.__pathinstance.getfp(), self.__fls.getfout())
    self.__fls.setoutm(7)  # set file mode as 'w' for write
    for host in root.iter('host'):
      ip = host.find('address').get('addr')  # ip address retrieveing
      ports = host.find('ports')  # searching for ports tag in host element
      for p in ports.iter('port'):  # searching for ports
        
        port = p.get('portid')
        state = p.find('state').get('state')

        # ignore all closed ports
        if state == 'open':

          if((i%self.__ips_bunch)==0 and i != counter):
            if i == 0:
              print '1) ===> Start'
            #create outfile instance
            os.chdir(self.__pathinstance.getfp())
            if(os.path.isfile(source)):
              os.remove(self.__fls.getfout())
            outf=open(self.__fls.getfout(), self.__fls.getoutm())
            print '2) ===> Output file is opend and ready for writing'

          outf.write(ip+':'+port+'\n')
          i += 1
          # scan out file when its ready
          if (((i%self.__ips_bunch) == 0 and i != 0) or i == counter):
            self.__scan(outf, self.__resdirname, bunch)
            bunch += 1
            os.chdir(self.__pathinstance.getcp())

  def __opensourcefile(self):
    # Open infile instance
    os.chdir(self.__pathinstance.getfp())
    source = "/"+self.__fls.getfin()
    if(os.path.isfile(os.getcwd() + source)):
      infile = open(self.__fls.getfin(), self.__fls.getinm())
    else:
      print "--> WARNING: Source file is not exist.\n--> WARNING: Make sure that ips.txt file is created."
      infile = None
    os.chdir(self.__pathinstance.getcp())
    return infile

  def __runscan(self, infile, ipoutnumber, ports, ips_bunch):
    # create outfiles and scann
    i=0
    bunch = 1
    source=os.path.join(self.__pathinstance.getfp(), self.__fls.getfout())
    #move file pointer to the start of file
    infile.seek(0,0)
    for line in infile:
      if ports is not None:
        ipmaker=ipp(line[0:-1], ports)
      else:
        ipmaker=ipp(line[0:-1])
      ipps=ipmaker.getipp()
      for x in ipps:
        if((i%ips_bunch)==0 and i != ipoutnumber):
          if i == 0:
            print '1) ===> Start'
          #create outfile instance
          os.chdir(self.__pathinstance.getfp())
          if(os.path.isfile(source)):
            os.remove(self.__fls.getfout())
          outfile=open(self.__fls.getfout(), self.__fls.getoutm())
          print '2) ===> Output file is opend and ready for writing'
        #populate outfile
        outfile.write(x+'\n')
        i += 1

        # scan out file when its ready
        if (((i%ips_bunch) == 0 and i != 0) or i == ipoutnumber):
          self.__scan(outfile, self.__resdirname, bunch)
          bunch += 1
    os.chdir(self.__pathinstance.getcp())

  def __scan(self, outfile, resdirn, bunch):
    print '3) ===> Preparation for scanning outputfile'
    #execute outputfile scan
    # Scann out.txt file using EyeWitness
    #close output file firest
    if(not outfile.closed):
      outfile.close()
      print '3.1)==> Output file is closed. Ready to scan.'
    outputfilepath = os.path.join(self.__pathinstance.getfp(), self.__fls.getfout())
    if bunch == 1:
        resdirname = resdirn
    if bunch > 1:
        resdirname = '%s_%d' % (resdirn, bunch)
    resultdir = os.path.join(self.__pathinstance.getfp(), "report", resdirname)
    eyewitness = os.path.join(self.__pathinstance.getcp(), 'EyeWitness', 'EyeWitness.py')
    #print '====> ' + eyewitness
    eyewitnessrun = 'python ' + eyewitness + ' -f ' + outputfilepath + ' -d ' + resultdir + ' --web'
    #print '====> ' + eyewitnessrun
    os.chdir(self.__pathinstance.getcp() + '/EyeWitness')
    print '3.2)==> Scanning...........'
    eyewitnessprocess = subprocess.Popen(eyewitnessrun, shell=True)
    eyewitnessprocess.wait()
    print '3.3)==> Scanning is done.'

  def runipconverter(self, sourcefile):

    # Open infile instance
    os.chdir(self.__pathinstance.getfp())
    source = "/"+self.__fls.getfin()
    self.__fls.setinm(7)
    
    filein = open(sourcefile, 'r')
    fileout = open(self.__fls.getfin(), self.__fls.getinm())

    fconv = Ipsconv(filein, fileout)
    fconv.convert()
    self.__resdirname = fconv.getheader()

    filein.close()
    fileout.close()

    os.chdir(self.__pathinstance.getcp())



