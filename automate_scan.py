import subprocess
import os
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEBase import MIMEBase
from email import encoders

#edit here
IP_RANGE = '192.168.0.1/24'
USER = "youremail@gmail.com"
PASSWORD = "yourpassword"
SCAN_PATH = "/tmp/vulnerability.xml"

def open_terminal(app_name, cmd):
	output = '[+] Executing ' + str(app_name) + '...\r\n'
	try:
		output += subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT)
		output += '\r\n'
	except Exception, e:
		output += str(e)
	output += '-------------------\r\n'

	return output


def execute_commands():
	#nmap
	commands = {"nmap infrastructure": "nmap -A -sV -v3 -Pn -oX " + SCAN_PATH + " --script http-vuln-cve2015-1635.nse --script-args vulns.showall " + IP_RANGE}
	result = ''

	for key, val in commands.items():
		output = open_terminal(key, val)
		result += output
	
	savelog = open('/tmp/vulnerability.log', 'w')
	savelog.write(result)
	savelog.close()	

	sendmail("Please see attached file.")
	return result

#Notify and send scan result as attachment
def sendmail(tosend):
	 
	msg = MIMEMultipart()
	 
	msg['From'] = USER
	msg['To'] = USER
	msg['Subject'] = "DAILY VULNERABILITY SCAN"

	 
	msg.attach(MIMEText(tosend, 'plain'))
	 
	filename = "vulnerability.xml"
	attachment = open(SCAN_PATH, "rb")
	 
	part = MIMEBase('application', 'octet-stream')
	part.set_payload((attachment).read())
	encoders.encode_base64(part)
	part.add_header('Content-Disposition', "attachment; filename= %s" % filename)
	 
	msg.attach(part)
	text = msg.as_string()

	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.starttls()
	server.login(USER, PASSWORD)
	server.sendmail(USER, USER, text)
	server.quit()

def main():
	#sendmail("yow!")
	execute_commands()

if __name__ == '__main__':
	main()
