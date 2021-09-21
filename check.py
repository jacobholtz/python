import sys
import colorama
from colorama import Fore
from colorama import Style
colorama.init()

# package = input("package: ")
# print(package)
try:
	# try to import the package specified
	# import package
	import requests
	# print success message
	print(Fore.GREEN + Style.NORMAL + "package installed" + Style.RESET_ALL)
except ModuleNotFoundError:
	print(Fore.RED + Style.BRIGHT + "package not installed" + Style.RESET_ALL)
