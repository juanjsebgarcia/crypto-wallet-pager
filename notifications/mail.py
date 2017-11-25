import json
import smtplib
import email
# this invokes the secure SMTP protocol (port 465, uses SSL)
from smtplib import SMTP as SMTP
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

try:
	email_SMTPSERVER = json.loads(open('settings.json', 'r').read())['Email_SMTPSERVER']
	email_USERNAME = json.loads(open('settings.json', 'r').read())['Email_USERNAME']
	email_PASSWORD = json.loads(open('settings.json', 'r').read())['Email_PASSWORD']
	email_FROMEMAIL = json.loads(open('settings.json', 'r').read())['Email_FROMEMAIL']
	email_activate = True
except:
	print("Email module failed to activate")

def mailsend(to, subject, content):
	'''
	Sends email securely using settings defined in settings.py
	'''
	
	text_subtype = 'plain'

	#BUILD EMAIL
	msg = MIMEMultipart()
	msg['From'] = email_FROMEMAIL
	msg['To'] = to+","
	msg['Subject'] = subject

	msg.attach(MIMEText(content, text_subtype))

	#SEND EMAIL
	conn = SMTP(email_SMTPSERVER, 587)
	conn.starttls()
	conn.set_debuglevel(False)
	conn.login(email_USERNAME, email_PASSWORD)

	try:
		conn.sendmail(email_FROMEMAIL, to, msg.as_string())
		return True
	except:
		print("Email failed to send, check email settings")
		return False
	finally:
		conn.quit()
