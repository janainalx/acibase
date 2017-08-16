import smtplib
from settings import USERMAIL, MAILPASS, TOMAIL
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import threading
import datetime
import time
import socket
from databases import insert_statistics, get_statistics
import urllib2 

def is_connected():
  #   try:
  #       # connect to the host -- tells us if the host is actually
  #       # reachable
		# socket.create_connection(("www.google.com", 80))
		# return True
  #   except OSError:
		# #print str(OSError)
  #   	return False

	try:
	    urllib2.urlopen("http://lafaiet.com")
	    return True
	except urllib2.URLError, e:
		return False



def send_mail(server, text):
	try:
		server.sendmail(USERMAIL, TOMAIL, text)
	except Exception as e:
		pass

	server.quit()


def send_statistics(message = None, time_spent = None):

	if message != None:
		insert_statistics(message, time_spent)
	
	if is_connected():
	# if True:
		print "Internet connection is OK"

		try:

			# server = smtplib.SMTP('smtpi.kinghost.net', 587)
			server = smtplib.SMTP('smtp.gmail.com', 587)
			server.starttls()
			server.login(USERMAIL, MAILPASS)
		except Exception as e:
			print(str(e))
			return

		stats = get_statistics()

		if len(stats) > 0:

			print "getting statistics from the database"

			stats_to_send = u""

			for st in stats:
				stats_to_send += st[0] + u"\n" + u"tempo gasto : " + str(st[1]) + u"\n\n"


			msg = MIMEMultipart()
			msg['From'] = USERMAIL
			msg['To'] = TOMAIL

			timestamp = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")

			msg['Subject'] = "Relatorio de jogo : " + timestamp

			body = MIMEText(stats_to_send.encode('utf-8'), 'plain', 'UTF-8')

			msg.attach(body)
			text = msg.as_string()

			print "sending email..."
			th = threading.Thread(target=send_mail, args=(server, text))
			th.start()
			print "mail sent!"

		else:
			print "Nothing to be sent..."


