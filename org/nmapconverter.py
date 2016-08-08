import xml.etree.ElementTree as ET

# 1. open nmap file
# 2. retriev ip address
# 3. retrieve ports
# 4. concatinate ip and ports
# 5. stor result into txt file
# 6. repeat for all ips
# 7. close all files


tree = ET.parse('urls.xml')  # parse xml file into tree
root = tree.getroot()  # get root element

# create output file instance
outfile = open('out.txt', 'w')
for host in root.iter('host'):
    ip = host.find('address').get('addr')  # ip address retrieveing
    ports = host.find('ports')  # searching for ports tag in host element
    for p in ports.iter('port'):  # searching for ports
        port = p.get('portid')
        state = p.find('state').get('state')
        if state == 'open':
            outfile.write(ip+':'+port+'\n')
outfile.close()
