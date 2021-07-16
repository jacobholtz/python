#!/bin/python3
# tutorial taken from https://www.thepythoncode.com/article/building-network-scanner-using-scapy
# network scanner written in python using scapy
# targets mapped via arp requests

import sys
import os
import requests
import colorama
from colorama import Fore
from colorama import Style
colorama.init()
# check if scapy is installed
try:
	import scapy
	pass
except ModuleNotFoundError:
	print(Fore.RED + Style.BRIGHT + "scapy not installed. installing..." + Style.RESET_ALL)
	os.system("pip3 install scapy")
	pass

from scapy.all import ARP, Ether, srp

# begin scanning
target_subnet = str(sys.argv[1]) # ip subnet to target
arp = ARP(pdst=target_subnet) # create the ARP packet
ether = Ether(dst="ff:ff:ff:ff:ff:ff") # create the ethernet broadcast packet
packet = ether/arp # create a whole arp and ethernet packet

# put all responses in a list of pairs in the format (sent_packet, received_packet)
reply = srp(packet, timeout=5)[0]

# create the client list
clients = []
for sent, received in reply:
	# for every reply, put the ip and mac addresses in the client list
	clients.append({'ip': received.psrc, 'mac': received.hwsrc})
# print the client list
print("Found devices:")
for client in clients:
	r = requests.get('http://searchmac.com/api/v2/' + client['mac'])
	oem = r.text
	print(Fore.GREEN + Style.NORMAL + "[+] " + Style.RESET_ALL + "IP: " + client['ip'] + " "*6 + " MAC: " + client['mac'] + " (" + oem + ")")