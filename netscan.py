#!/bin/python3
# tutorial taken from https://www.thepythoncode.com/article/building-network-scanner-using-scapy
# network scanner written in python using scapy
# targets mapped via arp requests

import sys
import os
import requests
import colorama
from colorama import Fore as F
from colorama import Style as S
colorama.init()
# check if scapy is installed
try:
	import scapy
	pass
except ModuleNotFoundError:
	print(F.RED + S.BRIGHT + "scapy not installed. installing..." + S.RESET_ALL)
	os.system("pip3 install scapy")
	pass

from scapy.all import ARP, Ether, srp

# check for arugments
if len(sys.argv) < 2:
	print(F.RED + S.BRIGHT + "[-] Usage: ./netscan.py host_ip/subnet" + S.RESET_ALL)
	quit()

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
	try:
		# try to get manufacturer
		r = requests.get('http://searchmac.com/api/v2/' + client['mac'])
		oem = r.text
		print(F.GREEN + S.NORMAL + "[+] " + S.RESET_ALL + "IP: " + client['ip'] + " "*6 + " MAC: " + client['mac'] + " (" + oem + ")")
	except ConnectionError:
		print(F.GREEN + S.NORMAL + "[+] " + S.RESET_ALL + "IP: " + client['ip'] + " "*6 + " MAC: " + client['mac'])
