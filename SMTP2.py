import sys
import os

#----------GLOBALS------------

#keep track of char in given line for sake of parsing
currentChar = 0

#What line am I expecting from the file: 0 = FROM, 1 = TO, 2 = TO || email body, 3 = email body || FROM
expectingLine = 0

#Have I sent out DATA command
sentDATA = False

#Do I need a response code from the standard input
needRespCode = False

#check if there is a command line argument
if len(sys.argv) != 2:
	sys.exit(1)

#input file from command line argument
forwardFile = sys.argv[1]

forwardFileList = list()

#Do I not skip printing the line
noSkip = True

#---------Helper and Parsing Functions---------

#iterate through chars in line
def nextChar():
	globals()["currentChar"] += 1
	return

#<white-space>
def parseWhiteSpace(code):
	if (code[globals()["currentChar"]] != ' ' and code[globals()["currentChar"]] != '\t'):
		return -2
	else:
		while(code[globals()["currentChar"]] == ' ' or code[globals()["currentChar"]] == '\t'):
			nextChar()
		return 1
	
#<arbitrary-text>
def parseArbitraryText(code):
	while(code[globals()["currentChar"]] != '\n'):
		nextChar()

#<CRLF>
def parseCRLF(code):
	if(code[globals()["currentChar"]] != '\n'):
		return -7
	return 1

#checks if line in file should generate MAIL FROM: command
def needFrom():
	if (line[0:5] == "From:"):
		return True
	else:
		return False
	
#checks if line in file should generate RCPT TO: command
def needTo():
	if (line[0:3] == 'To:'):
		return True
	else:
		return False
	
#this function will do one of two things: Send DATA command if it hasn't been sent OR Send email body if DATA has been sent. Doesn't need to check for next from command hopefully
def sendDATA():
	if sentDATA:
		globals()["needRespCode"] = False
		return line
	else:
		sys.stdout.write('DATA\n')
		globals()["noSkip"] = False
		globals()["sentDATA"] = True
		globals()["needRespCode"] = True
		return line

def parseResponseCode(code, data):
	globals()["currentChar"] = 0
	if data:
		accept354(code)
	else:
		accept250(code)
	parseWhiteSpace(code)
	parseArbitraryText(code)
	parseCRLF(code)

def accept250(code):
	if(code[globals()["currentChar"]] == "2"):
		nextChar()
	else:
		accept500plus()
	if(code[globals()["currentChar"]] == "5"):
		nextChar()
	else:
		accept500plus()
	if(code[globals()["currentChar"]] == "0"):
		nextChar()
	else:
		accept500plus()
	sys.stderr.write(respCode)

def accept354(code):
	if(code[globals()["currentChar"]] == "3"):
		nextChar()
	else:
		accept500plus()
	if(code[globals()["currentChar"]] == "5"):
		nextChar()
	else:
		accept500plus()
	if(code[globals()["currentChar"]] == "4"):
		nextChar()
	else:
		accept500plus()
	sys.stderr.write(respCode)

def accept500plus():
	sys.stderr.write(respCode)
	sys.stdout.write("QUIT\n")
	sys.exit(1)
#----------Main Code-----------

#copy the entirety of this file into a list. This way I only have to open the file once and can hopefully handle any errors separately
try:
	f = open(forwardFile, 'r')
	for linex in f:
		forwardFileList.append(linex)
except FileNotFoundError:
	sys.exit(1)

#iterate through lines in newly made array, call above functions accordingly
for line in forwardFileList:
	globals()["currentChar"] = 0
	#Generate, and emit to standard output, the appropriate SMTP server messages to send the email message(s) in the file to an SMTP server. 
	liney = ''
	needRespCode = False
	if needFrom():
		if(sentDATA == True):
			sys.stdout.write('.\n')
			sentDATA = False
			respCode = sys.stdin.readline()
			parseResponseCode(respCode, sentDATA)
		liney = 'MAIL FROM:' + line[5:]
		needRespCode = True
	elif needTo():
		liney = 'RCPT TO:' + line[3:]
		needRespCode = True
	else:
		liney = sendDATA()
	if noSkip:
		sys.stdout.write(liney)

	#After the output of each SMTP server message (except the QUIT message), wait for an SMTP response message to be received on standard input before proceeding. 
	if needRespCode:
		respCode = sys.stdin.readline()
		parseResponseCode(respCode, sentDATA)
	
	if noSkip == False:
		sys.stdout.write(liney)
	noSkip = True

#Generated all server messages except for the last period that will follow the last body of text. Loop has finished executing so should be goo to output just the period
sys.stdout.write('.\n')
respCode = sys.stdin.readline()
parseResponseCode(respCode, False)
sys.stdout.write("QUIT\n")