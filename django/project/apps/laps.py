import subprocess, sys, re, os
import phonetic_alphabet as alpha

POWERSHELLPATH = os.environ['POWERSHELLPATH']
POWERSHELLCMD = os.environ['POWERSHELLCMD']
AD_USER = os.environ['AD_USER']
AD_PASSWORD = os.environ['AD_PASSWORD']

def getLapsPassword(computer):
	password = ''
	p = subprocess.Popen([POWERSHELLPATH, '-ExecutionPolicy', 'Unrestricted', '-NoProfile', POWERSHELLCMD, AD_USER, AD_PASSWORD, computer]
				 , stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	
	(output, err) = p.communicate()
	p_status = p.wait()
	p.kill()
	if len(output) > 4:
		output = re.split(r'\s{2,}', output.decode())
		password = output[-3].split()[-1]

	return password

def convertPhonetically(text):
	string_builder = []
	for character in text:
		if character.isalnum():
			element = alpha.read(character)
			if character.islower(): element = element.lower()
		else: element = character
		string_builder = [element] + string_builder
	string_builder.reverse()
	return " ".join(string_builder)

