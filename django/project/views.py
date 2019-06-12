from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json, requests, os, time, hmac
from threading import Thread
from dotenv import load_dotenv

from project.apps import slack
from project.apps import laps

load_dotenv()
SLACK_SIGNING_SECRET = os.environ['SLACK_SIGNING_SECRET']
ALLOWED_SLACK_CHANNELS = os.environ['ALLOWED_SLACK_CHANNELS']
ALLOWED_SLACK_CHANNELS  = ALLOWED_SLACK_CHANNELS.split(",")

def homePageView(request):
	return HttpResponse('Hello, World!')

@csrf_exempt
def slackCommand(request):
	computer_name = response_url = None
	if request.method == 'POST':
		text = request.POST.get('text')
		response_url = request.POST.get('response_url')
		timestamp = request.headers.get('X-Slack-Request-Timestamp') 
		slack_signature = request.headers.get('X-Slack-Signature')
		version = 'v0'
		request_body = request.body.decode()

		channel = request.POST.get('channel_id')

		if channel not in ALLOWED_SLACK_CHANNELS:
			# This slack command not allowed to run from this channel
			# We should ignore this request.
			return HttpResponse('')

		if abs(time.time() - float(timestamp)) > 60 * 5:
			# The request timestamp is more than five minutes from local time.
			# It could be a replay attack, so let's ignore it and let it time out.
			return

		# Let's remake our Slack Signature and compare it
		sig_basestring = 'v0:' + timestamp + ':' + request_body
		my_signature = 'v0=' + slack.create_sha256_signature(SLACK_SIGNING_SECRET, sig_basestring)
		if hmac.compare_digest(my_signature, slack_signature):
			# hooray, the request came from Slack!
			if text == 'help':
				slack.get_help(response_url)
			else:
				# spawn thread to handle the request
				computer_name = text
				thr = Thread(target=slack.handle_slack_command, args=[computer_name,response_url])
				thr.start()
	# Reply 200 before Slack times out
	return HttpResponse('')