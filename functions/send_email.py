
# smtplib module send mail

import smtplib
import codecs

class Config_email_sender:

    def __init__(self):
        self.email = 'webecosmos@gmail.com'
        self.passw = '1qa2ws3ed-'

    def get_email(self):
        return self.email

    def get_passw(self):
        return self.passw

from email_templates import NEW_ACCOUNT_text, NEW_ACCOUNT_n_arg, NEW_ACCOUNT_html
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_email(to_email,title_email,args_ , type_email):
	try:
		msg = MIMEMultipart('alternative')
		if type_email == 'login':
			if len(args_) != NEW_ACCOUNT_n_arg:
				print('login_NO_ok')
				return False
			else:
				print('login_ok')
				msg['Subject'] = title_email
				text = NEW_ACCOUNT_text
				html = NEW_ACCOUNT_html % ("..........3333.3.3.3.3.3.")
		c = Config_email_sender()
		gmail_sender = c.get_email()
		gmail_passwd = c.get_passw()

		server = smtplib.SMTP('smtp.gmail.com', 587)
		server.ehlo()
		server.starttls()
		server.login(gmail_sender, gmail_passwd)

		me = c.get_email()
		you = to_email

		# Create message container - the correct MIME type is multipart/alternative.
		
		
		msg['From'] = me
		msg['To'] = you

		# Create the body of the message (a plain-text and an HTML version).
		
		print(type(NEW_ACCOUNT_html))
		

		# Record the MIME types of both parts - text/plain and text/html.
		part1 = MIMEText(text, 'plain')
		part2 = MIMEText(html, 'html')

		# Attach parts into message container.
		# According to RFC 2046, the last part of a multipart message, in this case
		# the HTML message, is best and preferred.
		msg.attach(part1)
		msg.attach(part2)

		# Send the message via local SMTP server.
		# sendmail function takes 3 arguments: sender's address, recipient's address
		# and message to send - here it is sent as one string.
		server.sendmail(me, you, msg.as_string())
		server.quit()
		print('enviado exitosamente')
	except Exception as e:
		print(e)

if __name__ == '__main__':
	send_email("fverbo.tkd@gmail.com", "Bienvenido a gonsa2", ['esto es un email'], 'login')