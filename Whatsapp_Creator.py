import urllib
import json
import time
import os
import math

__author__ = 'Lambasoft'
__website__ = "onlinesmsverification.xyz"
__version__ = "1.0"

api_url = "http://api.onlinesmsverification.xyz/api.php" # Do not change this unless you know what you're doing
osms_token = "" # Place your http://onlinesmsverification.xyz token here
max_tries = 3 # Do not change that or your account will get automatically banned
save_path = ""

def apiAction( action , parameter = ""):
	fetch_url = api_url + "?token=" + osms_token + "&action=" + action + parameter
	f = urllib.urlopen(fetch_url)
	html = f.read()
	return html

def find_between( s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""


def setProxies():
    isValid = False
    while not isValid:
        answer = raw_input("Enter proxies:port txt file path : \r\n")
	if answer:
		if ".txt" in answer:
		    if os.path.isfile(answer):
		        with open(answer, 'r') as f:
		            results = f.read().splitlines()
		            return results
		        isValid = True
		    else:
		        print "[!] Please make sure the file exist"
		        isValid = False
		else:
		    print "Proxies should be in a .txt file"
		    isValid = False
	else:
		isValid = True
		return []


if __name__ == "__main__":
	print " " * 9 + "-" * 42
	print " " * 10 + "Author: {0} | {1}".format(__author__ , __website__)
	print " " * 20 + "WhatsApp Mass Creator"
	print " " * 25 + "Version: {0} ".format(__version__)
	print " " * 9 + "-" * 42
	print "\n\r"

	if not osms_token:
       		osms_token = raw_input("Enter your Token: ")

	data = json.loads(apiAction("balance"))
	print "Your Balance is: {0}".format(data['balance'])

	account_count = 0
	while (account_count <= 0):
		account_count = input("How many WhatsApp Accounts would you like to create?\r\n")

	proxies = setProxies()
	while (len(proxies) < account_count):
		print "Loaded " + str(len(proxies)) + " proxies."
		print "Proxies should be more than accounts!"
		proxies = setProxies()
	
	print "Loaded " + str(len(proxies)) + " proxies."

	while (not save_path):
		save_path = raw_input("Enter Output File Name:\r\n")

	print "Accounts will be saved to " + os.path.dirname(os.path.realpath("__file__")) + "/" + save_path
	save_path = os.path.dirname(os.path.realpath("__file__")) + "/" + save_path

	print "Creating Accounts ..."
	counter = 0
	while (account_count > 0 and max_tries >0):
		proxy = proxies[counter]
		print "Loaded proxy: " + proxy
		result = json.loads(apiAction("getMobile","&pid=3"))
		number = 0
		if(result['success']):
			number = result['number']
			time.sleep(10) # Do not change that or your account will get automatically banned
			print "Fetched number: " + number
		else:
			print "Error '" + result['error'] + "' fetching number, retrying ..."
			time.sleep(10) # Do not change that or your account will get automatically banned
			max_tries -= 1 # Do not change that or your account will get automatically banned
			continue

		result = json.loads(apiAction("wapCode","&number={0}&proxy={1}".format(number,proxy)))
		if(result['success']):
			print "Code successfully sent to " + number
		else:
			print "Error '" + result['error'] + "' sending SMS retrying with new number..."
			time.sleep(10) # Do not change that or your account will get automatically banned
			max_tries -= 1 # Do not change that or your account will get automatically banned
			continue

		sms_code = ""
		sms_tries = 0
		while (not sms_code and sms_tries < 5):
			print "[{0}] Attempting to receive SMS ...".format(sms_tries+1)
			time.sleep(10) # Do not change that or your account will get automatically banned
			result = json.loads(apiAction("getSMS","&pid=3&number="+number))
			if(result['success'] and result['received']):
				sms_code = find_between(result['message'].lower(),"whatsapp code",".").strip()
				print "Received Code: " + sms_code
			sms_tries+=1

		if(not sms_code):
			print "Failed receiving SMS Code, retrying with new number..."
			time.sleep(10) # Do not change that or your account will get automatically banned
			max_tries -= 1 # Do not change that or your account will get automatically banned
			counter+=1
			continue
	
		result = json.loads(apiAction("wapVerCode","&code={0}&number={1}&proxy={2}".format(sms_code,number,proxy)))
		if(result['success']):
			print "Successfully Created Account\r\n{0}\r\n{1}".format(result['username'],result['password'])
			f = open(save_path,'w+')
			f.write(result['username'] + ":" + result['password'] + "\n")
			f.close()
			account_count -= 1
			max_tries = 3
			counter+=1
		else:
			print "Error: " + result['error']
		
		
	if (max_tries <= 0):
		print "Too many consecutive fails, exiting..."
	
		
