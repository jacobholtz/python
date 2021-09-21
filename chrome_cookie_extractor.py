#!/bin/python3
# tutorial taken from https://www.thepythoncode.com/article/building-network-scanner-using-scapy
# this script extracts cookies from google chrome in windows

import pycryptodome, pypiwin32, json, base64, sqlite3, shutil, win32crypt
import sys, os, colorama
from datetime import datetime, timedelta
from Crypto.Cipher import AES
from colorama import Fore as F
from colorama import Style as S
colorama.init()

# check if packages are installed
# pywin32 will need to be installed manually at https://pypi.org/project/pypiwin32/#files
try:
	import colorama, pycryptodome, pypiwin32, json, base64, sqlite3, shutil, datetime, win32crypt
	pass
except ModuleNotFoundError:
	print(F.RED + S.BRIGHT + "modules not installed. installing..." + S.RESET_ALL)
	os.system("pip3 install colorama pycryptodome")
	pass