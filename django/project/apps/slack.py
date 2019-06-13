import hmac, hashlib, requests, json
from project.apps import laps



def get_help(response_url):
	response = {
		"text": "To use this Slack command, type in the Active Directory computer name after your command. The computer name is not case sensitive, but the password is. Try,",
		"attachments": [
			{
				"text": "/laps G6PKGX1"
			}
		]
	}
	requests.post(response_url, data=json.dumps(response))

def handle_slack_command(computer_name, response_url):
	password = laps.getLapsPassword(computer_name)
	message = "Not Found. Either the password is not stored in LAPS or the computer is not Active Directory."

	if len(password) > 0: 
		password_phonetically = laps.convertPhonetically(password)
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

def create_sha256_signature(key, message):
	message = bytes(message, 'utf-8')
	byte_key = bytes(key, 'utf-8')
	return hmac.new(byte_key, message, hashlib.sha256).hexdigest()

