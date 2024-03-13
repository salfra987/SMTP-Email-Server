import sys
 
currentChar = 0


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

def responseCodes(err):
	if (err == 1):
		return 'Sender ok'
	if (err == -1):
		return 'ERROR -- mail-from-cmd'
	if (err == -2):
		return 'ERROR -- whitespace'
	if (err == -3):
		return 'ERROR -- path'
	if (err == -4):
		return 'ERROR -- mailbox'
	if (err == -5):
		return 'ERROR -- string'
	if (err == -6):
		return 'ERROR -- element'
	if (err == -7):
		return 'ERROR -- CRLF'
	else:
		return 'it should not be possible to recieve this error'

for line in sys.stdin:
	
	sys.stdout.write(line)

	sys.stdout.write(responseCodes(parseMailFromCmd()) + '\n')