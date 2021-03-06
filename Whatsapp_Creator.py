import urllib
import json
import time
import os
import math

__author__ = 'Lambasoft'
__website__ = "onlinesmsverification.xyz"
__version__ = "1.0"

debug = True
api_url = "http://api.onlinesmsverification.xyz/api.php" # Do not change this unless you know what you're doing
osms_token = "" # Place your http://onlinesmsverification.xyz token here
max_tries = 5 # Maximum number of failed tries per registration before we stop trying
save_path = ""

#Do not edit anything from below
reason = {
	'bad_proxy' : False
};

counter = {
	'bad_proxy' : 0,
	'accounts' : 0,
	'sms_tries' : 0,
	'created_accounts' :0,
	'tries' : 0,
	"proxy" : 0
};
number = 0

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
	print "We only accept proxies using the following ports: {80,8080}"
        answer = raw_input("Enter proxies:port txt file path : \r\n")
	if answer:
		if ".txt" in answer:
		    if os.path.isfile(answer):
		        with open(answer, 'r') as f:
		            results = f.read().splitlines()
		            return [ x for x in results if (":80" or ":8080") in x ]
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

	while (counter['accounts'] <= 0):
		counter['accounts'] = input("How many WhatsApp Accounts would you like to create?\r\n")

	proxies = setProxies()
	while (len(proxies) < counter['accounts']):
		print "Loaded " + str(len(proxies)) + " proxies."
		print "Proxies should be more than accounts!"
		proxies = setProxies()
	
	print "Loaded " + str(len(proxies)) + " proxies."

	while (not save_path):
		save_path = raw_input("Enter Output File Name:\r\n")

	print "Accounts will be saved to " + os.path.dirname(os.path.realpath("__file__")) + "/" + save_path + ".txt"
	save_path = os.path.dirname(os.path.realpath("__file__")) + "/" + save_path + ".txt"

	print "Creating Accounts ..."
	while (counter['accounts'] > 0 and counter['tries'] <= max_tries):
		if (proxies[counter['proxy']]):
			proxy = proxies[counter['proxy']]
		else:
			print "No more proxies..."
			break;

		print "Loaded proxy: " + proxy

		if(reason['bad_proxy'] == False):
			time.sleep(10) # Do not change that or your account will get automatically banned
			result = json.loads(apiAction("getMobile","&pid=3"))
			if(result['success']):
				counter['tries'] = 0
				number = result['number']
				print "Fetched number: " + number
			else:
				print "Error" + ((" '" + str(result['error']) + "' ") if debug == True else " ") + "fetching number, retrying ..."
				time.sleep(10) # Do not change that or your account will get automatically banned
				continue


		
		time.sleep(10) # Do not change that or your account will get automatically banned
		result = json.loads(apiAction("wapCode","&number={0}&proxy={1}".format(number,proxy)))
		if(result['success']):
			print "Code successfully sent to " + number
		elif result['error'] == "There was a problem trying to request the code":
			print "Error" + ((" '" + str(result) + "' ") if debug == True else " ") + "while sending SMS to " + str(number) + " retrying with new number..."
			reason['bad_proxy'] = False
			counter['tries'] += 1
			continue
		else:
			print "Error" + ((" '" + str(result['error']) + "' ") if debug == True else " ") + "while sending SMS to " + str(number) + " retrying with new proxy..."
			reason['bad_proxy'] = True
			counter['tries'] += 1
			counter['proxy'] += 1
			continue

		sms_code = ""
		while (not sms_code and counter['sms_tries'] < 5):
			print "[{0}] Attempting to receive SMS ...".format(counter['sms_tries']+1)
			time.sleep(15) # Do not change that or your account will get automatically banned
			result = json.loads(apiAction("getSMS","&pid=3&number="+number))
			if(result['success'] and result['received']):
				sms_code = find_between(result['message'].lower(),"whatsapp code",".").strip()
				print "Received Code: " + sms_code
			counter['sms_tries'] += 1

		if(not sms_code):
			print "Failed receiving SMS Code, retrying with new number..."
			time.sleep(10) # Do not change that or your account will get automatically banned
			counter['tries'] += 1
			continue
	

		time.sleep(10) # Do not change that or your account will get automatically banned
		result = json.loads(apiAction("wapVerCode","&code={0}&number={1}&proxy={2}".format(sms_code,number,proxy)))
		if(result['success']):
			print "Successfully Created Account\r\n{0}\r\n{1}".format(result['username'],result['password'])
			f = open(save_path,'a+')
			f.write(result['username'] + ":" + result['password'] + "\n")
			f.close()
			counter['accounts'] -= 1
			counter['created_accounts'] += 1
			counter['tries'] = 0
			counter['sms_tries'] = 0
			reason['bad_proxy'] = False
			counter['proxy'] += 1
		else:
			print "Error: " + result['error']
		
		
	if (counter['tries'] >= max_tries):
		print "Too many consecutive fails, exiting..."
	
		
