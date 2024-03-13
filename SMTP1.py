import sys
import os

currentChar = 0

leftChar = 0
rightChar = 0

mailFromIn = False


#iterate through chars in line
def nextChar():
	globals()["currentChar"] += 1
	return

#<mail-from-cmd> ::= “MAIL” <whitespace> “FROM:” <nullspace> <reverse-path> <nullspace> <CRLF>
def parseMailFromCmd():
	globals()["currentChar"] = 0
	#mail
	if(line[globals()["currentChar"]] == 'M'):
		nextChar()
	else:
		return -1
	if(line[globals()["currentChar"]] == 'A'):
		nextChar()
	else:
		return -1
	if(line[globals()["currentChar"]] == 'I'):
		nextChar()
	else:
		return -1
	if(line[globals()["currentChar"]] == 'L'):
		nextChar()
	else:
		return -1
	#whiteSpace now differs from HW1 parse, this whitespace will throw a 500 error not a whitespace error
	x = parseWhitespace()
	if(x != 1):
		return -1
	#from:
	if(line[globals()["currentChar"]] == "F"):
		nextChar()
	else:
		return -1
	if(line[globals()["currentChar"]] == "R"):
		nextChar()
	else:
		return -1
	if(line[globals()["currentChar"]] == "O"):
		nextChar()
	else:
		return -1
	if(line[globals()["currentChar"]] == "M"):
		nextChar()
	else:
		return -1
	if(line[globals()["currentChar"]] == ":"):
		nextChar()
	else:
		return -1
	#nullspace
	b = parseNullspace()
	if(b != 1):
		return b
	#reversepath
	c = parseReversePath()
	if(c != 1):
		return c
	#nullspace
	d = parseNullspace()
	if(d != 1):
		return d
	#CRLF
	e = parseCRLF()
	if(e != 1):
		return e
	return 1
	
def parseWhitespace():
	if (line[globals()["currentChar"]] != ' ' and line[globals()["currentChar"]] != '\t'):
		return -2
	else:
		while(line[globals()["currentChar"]] == ' ' or line[globals()["currentChar"]] == '\t'):
			nextChar()
		return 1

def parseNullspace():
	while(line[globals()["currentChar"]] == ' ' or line[globals()["currentChar"]] == '\t'):
			nextChar()
	return 1

def parseReversePath():
	return parsePath()

def parsePath():
	if(line[globals()["currentChar"]] != '<'):
		return -3
	nextChar()
	y = parseMailbox()
	if(y != 1):
		return y
	if(line[globals()["currentChar"]] != '>'):
		return -3
	nextChar()
	return 1

def parseMailbox():
	z = parseLocalPart()
	if(z != 1):
		return z
	if(line[globals()["currentChar"]] != '@'):
		return -4
	nextChar()
	a = parseDomain()
	if(a != 1):
		return a
	return 1

def parseLocalPart():
	f = parseMyString()
	if(f != 1):
		return f
	return 1

def parseMyString():
	if(isChar(line[globals()["currentChar"]]) == False):
		return -5
	while(isChar(line[globals()["currentChar"]]) == True):
		nextChar()
	return 1

def isChar(thisChar):
	if(isSpecial(thisChar)):
		return False
	if(isSpace(thisChar)):
		return False
	if(ord(thisChar) < 126 and ord(thisChar) > 33):
		return True
	return False

def isSpecial(thisChar):
	if (thisChar == '<'):
		return True
	if (thisChar == '>'):
		return True
	if (thisChar == '('):
		return True
	if (thisChar == ')'):
		return True
	if (thisChar == '['):
		return True
	if (thisChar == ']'):
		return True
	if (thisChar == '\\'):
		return True
	if (thisChar == '.'):
		return True
	if (thisChar == ','):
		return True
	if (thisChar == ';'):
		return True
	if (thisChar == ':'):
		return True
	if (thisChar == '@'):
		return True
	if (thisChar == '\"'):
		return True
	return False

def isSpace(thisChar):
	if (thisChar == ' ' or thisChar == '\t'):
		return True
	return False

def parseDomain():
	g = parseElement()
	if(g != 1):
		return g
	if(line[globals()["currentChar"]] == '.'):
		nextChar()
		h = parseDomain()
		if(h != 1):
			return h
	return 1

def parseElement():
	if(isLetter(line[globals()["currentChar"]])):
		nextChar()
	else:
		return -6
	while(isLetDigStr(line[globals()["currentChar"]])):
		nextChar()
	return 1

def isLetter(thisChar):
	if(ord(thisChar) >= 97):
		if(ord(thisChar) <= 122):
			return True
	if(ord(thisChar) >= 65):
		if(ord(thisChar) <= 90):
			return True
	return False

def isLetDigStr(thisChar):
	return(isLetter(thisChar) or isDig(thisChar))

def isDig(thisChar):
	return(ord(thisChar) >= 48 and ord(thisChar) <= 57)

def parseCRLF():
	if(line[globals()["currentChar"]] != '\n'):
		return -7
	return 1

#expectingCmd should be set to 1 when expecting MAIL FROM in input, 2 when expecting RCPT TO in input, 3 when expecting DATA in input, 4 when expecting message body or <CRLF>.<CRLF>, 0 reserved for a state you didn't expect the program to reach
expectingCmd = 1

#global for checking whether or not we can stop recieveing the incoming message 0 means nothing recieved, 1 means first <CRLF> recieved, 2 means period recieved, 3 means second <CRLF> recieved
recievedPeriod = 0

#number of recipients
recievers = 0
receiveList = list()

#What we want to put in the forward/forward-path-n files
text = list()

#Who is sending message
senderPath = ''

# <rcpt-to-cmd> ::= “RCPT” <whitespace> “TO:” <nullspace> <forward-path> <nullspace> <CRLF>
def parseRCPTTOCmd():
	globals()["currentChar"] = 0
    #RCPT
	if(line[globals()["currentChar"]] == 'R'):
		nextChar()
	else:
		return -1
	if(line[globals()["currentChar"]] == 'C'):
		nextChar()
	else:
		return -1
	if(line[globals()["currentChar"]] == 'P'):
		nextChar()
	else:
		return -1
	if(line[globals()["currentChar"]] == 'T'):
		nextChar()
	else:
		return -1
	#Whitespace
	x = parseWhitespace()
	if(x != 1):
		return -1
	#TO:
	if(line[globals()["currentChar"]] == 'T'):
		nextChar()
	else:
		return -1
	if(line[globals()["currentChar"]] == 'O'):
		nextChar()
	else:
		return -1
	if(line[globals()["currentChar"]] == ':'):
		nextChar()
	else:
		return -1
	#nullspace
	y = parseNullspace()
	if(y != 1):
		return y
	#forward-path
	globals()["leftChar"] = globals()["currentChar"] + 1
	z = parseForwardPath()
	if(z != 1):
		return z
	globals()["rightChar"] = globals()["currentChar"] - 1
	#nullspace
	a = parseNullspace()
	if(a != 1):
		return a
	#CRLF
	b = parseCRLF()
	if(b != 1):
		return b
	return 1

#<forward-path> ::= <path>
def parseForwardPath():
	c = parsePath()
	if(c != 1):
		return c
	return 1

#<data-cmd> ::= “DATA” <nullspace> <CRLF>
def parseDataCmd():
	globals()["currentChar"] = 0
	#data
	if(line[globals()["currentChar"]] == 'D'):
		nextChar()
	else:
		return -1
	if(line[globals()["currentChar"]] == 'A'):
		nextChar()
	else:
		return -1
	if(line[globals()["currentChar"]] == 'T'):
		nextChar()
	else:
		return -1
	if(line[globals()["currentChar"]] == 'A'):
		nextChar()
	else:
		return -1
	#nullspace
	d = parseNullspace()
	if(d != 1):
		return d
	#CRLF
	e = parseCRLF()
	if(e != 1):
		return e
	return 2

def acceptMessageBody():
	if(line == "In other cases, EOF may be used to indicate the end of a stream of data, such as a network connection.\n"):
		return 72
	if(line == '.\n' or line == '\r.\n'):
		return 1
	else:
		return -1

def responseCodes(err):
	if (err == 1):
		return '250 OK'
	if (err == 2):
		return '354 Start mail input; end with <CRLF>.<CRLF>'
	if (err == 3):
		return '503 Bad sequence of commands'
	if (err == -1):
		return '500 Syntax error: command unrecognized'
	if (err == -2):
		return '501 Syntax error in parameters or arguments'
	if (err == -3):
		return '501 Syntax error in parameters or arguments'
	if (err == -4):
		return '501 Syntax error in parameters or arguments'
	if (err == -5):
		return '501 Syntax error in parameters or arguments'
	if (err == -6):
		return '501 Syntax error in parameters or arguments'
	if (err == -7):
		return '501 Syntax error in parameters or arguments'
	else:
		return 'you should not be recieving this error'
	
for line in sys.stdin:
	#print out input
	sys.stdout.write(line)
	#helper to skip lines if bad code is in expectingCmd
	end = False
	#check which cmd I should recieve next and then attempt to parse it
	if (globals()["expectingCmd"] == 4 and end == False):
		i = acceptMessageBody()
		#1 response code means <CRLF>.<CRLF> was just seen
		if(i == 1):
			globals()["mailFromIn"] = False
			sys.stdout.write(responseCodes(i) + '\n')
			end = True
			#This function will take the now completed block of text and append all lines to the now known n number of files
			thisDir = os.path.dirname(os.path.realpath(__file__))
			pathToForward = os.path.join(thisDir, 'forward')
			if not os.path.exists(pathToForward):
				os.makedirs(pathToForward)
			for liney in receiveList:
				pathy = ''
				f = open(pathToForward + "/" + liney, "a")
				for linex in text:
					f.write(linex)
				f.close()
			globals()["expectingCmd"] = 1
			globals()["text"].clear()
			globals()["receiveList"].clear()
			globals()["recievers"] = 0
		elif(i == 72):
			end = True 
			globals()["expectingCmd"] = 1
			sys.stdout.write(responseCodes(-6) + '\n')
		else:
			text.append(line)
			end = True
			globals()["expectingCmd"] = 4
	if (globals()["expectingCmd"] == 3 and end == False):
		h = parseDataCmd()
		if(h == 2):
			sys.stdout.write(responseCodes(h) + '\n')
			globals()["expectingCmd"] = 4
		elif(h == -1):
			if(parseMailFromCmd() == -1):
				if(parseRCPTTOCmd() == 1):
					globals()["expectingCmd"] = 2
				else:
					skip = False
					globals()["currentChar"] = 0
					#RCPT
					if(line[globals()["currentChar"]] == 'R' and skip == False):
						nextChar()
					else:
						sys.stdout.write(responseCodes(-1) + '\n')
						skip = True
					if(line[globals()["currentChar"]] == 'C' and skip == False):
						nextChar()
					elif(skip == False):
						sys.stdout.write(responseCodes(-1) + '\n')
						skip = True
					if(line[globals()["currentChar"]] == 'P' and skip == False):
						nextChar()
					elif(skip == False):
						sys.stdout.write(responseCodes(-1) + '\n')
						skip = True
					if(line[globals()["currentChar"]] == 'T' and skip == False):
						nextChar()
					elif(skip == False):
						sys.stdout.write(responseCodes(-1) + '\n')
						skip = True
					#Whitespace
					if(skip == False):
						x = parseWhitespace()
						if(x != 1):
							sys.stdout.write(responseCodes(-1) + '\n')
							skip = True
					#TO:
					if(line[globals()["currentChar"]] == 'T' and skip == False):
						nextChar()
					elif(skip == False):
						sys.stdout.write(responseCodes(-1) + '\n')
						skip = True
					if(line[globals()["currentChar"]] == 'O' and skip == False):
						nextChar()
					elif(skip == False):
						sys.stdout.write(responseCodes(-1) + '\n')
						skip = True
					if(line[globals()["currentChar"]] == ':' and skip == False):
						nextChar()
					elif(skip == False):
						sys.stdout.write(responseCodes(-1) + '\n')
						skip = True
					if(skip == True):
						globals()["expectingCmd"] = 1
						end = True
					else:
						globals()["expectingCmd"] = 2
			else:
				sys.stdout.write(responseCodes(3) + '\n')
				globals()["expectingCmd"] = 1
				end = True
		else:
			globals()["expectingCmd"] = 1
			sys.stdout.write(responseCodes(h) + '\n')
	if (globals()["expectingCmd"] == 2 and end == False):
		g = parseRCPTTOCmd()
		if(g == 1):
			receiveList.append(line[leftChar:rightChar])
			sys.stdout.write(responseCodes(g) + '\n')
			j = 0
			k = line[j]
			while (k != '<'):
				j += 1
				k = line[j]
			text.append("To: " + line[j:-1] + '\n')
			globals()["expectingCmd"] = 3
			globals()["recievers"] += 1
		elif(g == -1):
			if(parseDataCmd() == -1):
				if(parseMailFromCmd() != -1):
					sys.stdout.write(responseCodes(3) + '\n')
				else:
					sys.stdout.write(responseCodes(g) + '\n')
			else:
				sys.stdout.write(responseCodes(3) + '\n')
			globals()["expectingCmd"] = 1
		else:
			globals()["expectingCmd"] = 1
			sys.stdout.write(responseCodes(g) + '\n')
		end = True
	if (globals()["expectingCmd"] == 1 and end == False):
		f = parseMailFromCmd()
		if(f == 1):
			sys.stdout.write(responseCodes(f) + '\n')
			l = 0
			m = line[l]
			while (m != '<'):
				l += 1
				m = line[l]
			if(globals()["mailFromIn"] == False):
				text.append("From: " + line[l:-1] + '\n')
				globals()["mailFromIn"] = True
			globals()["expectingCmd"] = 2
		elif(f == -1):
			if(parseDataCmd() == -1):
				if(parseRCPTTOCmd() != -1):
					sys.stdout.write(responseCodes(3) + '\n')
				else:
					sys.stdout.write(responseCodes(f) + '\n')
			else:
				sys.stdout.write(responseCodes(3) + '\n')
			globals()["expectingCmd"] = 1
		else:
			globals()["expectingCmd"] = 1
			sys.stdout.write(responseCodes(f) + '\n')
		end = True