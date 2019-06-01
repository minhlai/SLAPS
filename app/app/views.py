from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json, requests, os
from threading import Thread
import time, hmac, hashlib
import phonetic_alphabet as alpha
from dotenv import load_dotenv

load_dotenv()
SLACK_SIGNING_SECRET = os.environ['SLACK_SIGNING_SECRET']
AD_USER = os.environ['AD_USER']
AD_PASSWORD = os.environ['AD_PASSWORD']

def homePageView(request):
	return HttpResponse('Hello, World!')
	
def slackEventSubscription(request):
	challenge = None
	body_unicode = request.body.decode('utf-8')
	body = json.loads(body_unicode)
	if body['type'] == 'url_verification':
		challenge = body['challenge']
	return JsonResponse({'challenge': challenge})

@csrf_exempt
def slackCommand(request):
	computer_name = response_url = None
	if request.method == 'POST':
		computer_name = request.POST.get('text')
		response_url = request.POST.get('response_url')
		timestamp = request.headers.get('X-Slack-Request-Timestamp') 
		slack_signature = request.headers.get('X-Slack-Signature')
		version = 'v0'
		request_body = request.body.decode()
		if abs(time.time() - float(timestamp)) > 60 * 5:
			# The request timestamp is more than five minutes from local time.
			# It could be a replay attack, so let's ignore it.
			return

		# Let's remake our Slack Signature and compare it
		sig_basestring = 'v0:' + timestamp + ':' + request_body
		my_signature = 'v0=' + create_sha256_signature(SLACK_SIGNING_SECRET, sig_basestring)
		if hmac.compare_digest(my_signature, slack_signature):
			# hooray, the request came from Slack!
			thr = Thread(target=handle_slack_command, args=[computer_name,response_url])
			thr.start()

	response = {
		'status': 200
	}
	# return HttpResponse(json.dumps(response), content_type="application/json")
	return HttpResponse('')


def handle_slack_command(computer_name, response_url):
	password = getLapsPassword(computer_name)
	message = "Not Found. Either the password is not stored in LAPS or the computer is not Active Directory."

	if len(password) > 0: 
		password_phonetically = convertPhonetically(password)
		message = "{0}\r\n{1}".format(password, password_phonetically)

	response = {
		"text": "The password for {} is: ".format(computer_name),
		"attachments": [
			{
				"text": message
			}
		]
	}

	requests.post(response_url, data=json.dumps(response))


import subprocess, sys, re

def getLapsPassword(computer):
	password = ''
	expiration = ''
	# TODO do some exception handling here for system args
	# if len(sys.argv) > 1: computer = sys.argv[1]
	# else: exit()

	p = subprocess.Popen(["powershell.exe", 
				  "C:\\Users\\laim\\Desktop\\SLAPS\\laps.ps1 {0} {1} {2}".format(AD_USER, AD_PASSWORD, computer)], stdout=subprocess.PIPE)
				  # "C:\\Users\\laim\\Desktop\\SLAPS\\laps.ps1 {}".format(computer)], stdout=subprocess.PIPE)
	(output, err) = p.communicate()
	p_status = p.wait()

	if len(output) > 0:
		output = re.split(r'\s{2,}', output.decode())
		password = output[-3].split()[-1]
		expiration = output[-2:]
	print(expiration)

	# print("Command output : {}".format(password))
	# print("Command exit status/return code : {}".format(p_status))
	return password

def convertPhonetically(text):
	string_builder = []
	for character in text:
		if character.isalnum():
			element = alpha.read(character)
			if character.islower(): element = element.lower()
		else: element = character
		string_builder = [element] + string_builder
	print(string_builder)
	string_builder.reverse()
	return " ".join(string_builder)

def create_sha256_signature(key, message):
	message = bytes(message, 'utf-8')
	byte_key = bytes(key, 'utf-8')
	return hmac.new(byte_key, message, hashlib.sha256).hexdigest()

