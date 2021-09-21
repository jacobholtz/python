#!/bin/python3
# tutorial taken from https://www.thepythoncode.com/article/sql-injection-vulnerability-detector-in-python
# sql injection written in python3 using beutifiulsoup
# TODO:
# implement https://github.com/sqlmapproject/sqlmap/blob/master/data/xml/errors.xml xml error page as sql errors


import os, sys
import colorama
from colorama import Fore
from colorama import Style
colorama.init()

# check if bs4 and requests are installed
try:
	import bs4, requests
	pass
except ModuleNotFoundError:
	print(Fore.RED + Style.BRIGHT + "BeautifulSoup4 or requests are not installed. installing..." + Style.RESET_ALL)
	os.system("pip3 install bs4 requests")
	pass

# begin code
from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin
from pprint import pprint

# start an http session, set the browser
s = requests.Session()
s.headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36"

# define functions needed to extract html forms
def get_all_forms(url):
	# returns all forms from a url
	soup = bs(s.get(url).content, "html_parser")
	return soup.find_all("form")

def get_form_details(form):
	# extracts useful form information
	details = {}
	try:
		action = form.attrs.get("action").lower()
	except:
		action = None
	# determine form method
	method = form.attrs.get("method", "get").lower()
	# get all inputs such as type and name
	inputs = []
	for input_tag in form.find_all("input"):
		input_type = input_tag.attrs.get("type", "text")
		input_name = input_tag.attrs.get("name")
		input_value = input_tag.attrs.get("value", "")
		inputs.append({"type": input_type, "name": input_name, "value": input_value})
	# put everything into the details dictionary
	details["action"] = action
	details["method"] = method
	details["inputs"] = inputs
	return details

def sql_check(response):
	# a boolean function that checks for SQLi based on its response
	errors = {
		# mysql
		"you have an error in your sql syntax;",
		"warning: mysql",

		# sql server
		"unclosed quotation mark after the character string",

		# oracle
		"quoted string not properly terminated"
	}
	for error in errors:
		# return true if an error is found
		if error in response.content.decode().lower():
			return True
	# otherwise, no error is found
	return False

def scan_sqli(url):
	# scan for sqli on the given url
	for c in "\"'":
		# adds a quote and double quote character to the url
		new_url = f"{url}{c}"
		print("[!] Trying ", new_url)
		# make the http request
		res = s.get(new_url)
		if sql_check(res):
			# sql detection on the url itself
			print("[+] SQL Injection vulnerability detected at: ", new_url)
			return
	# scan for sqli in html forms
	forms = get_all_forms(url)
	print(f"[+] Detected {len(forms)} forms on {url}.")
	for form in forms:
		form_details = get_form_details(form)
		for c in "\"'":
			# data body to submit
			data = {}
			for input_tag in form_details["inputs"]:
				if input_tag["type"] == "hidden" or input_tag["value"]:
					# use any input form in the body
					try:
						data[input_tag["name"]] = input_tag["value"] + c
					except:
						pass
				elif input_tag["type"] != "submit":
					# use junk data on everything except submit
					data[input_tag["name"]] = f"test{c}"
			# join the url with the action
			url = urljoin(url, form_details["action"])
			if form_details["method"] == "post":
				res = s.post(url, data=data)
			elif form_details["method"] == "get":
				res = s.get(url, params=data)
			# test for vulnerability(res):
			if sql_check(res):
				print("[+] SQL Injection vulnerability detected at ", url)
				print("[+] Form:")
				pprint(form_details)
				break

if __name__ == "__main__":
	url = sys.argv[1]
	print(sys.argv[1])
	scan_sqli(url)
