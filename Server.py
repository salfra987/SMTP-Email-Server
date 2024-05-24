# I have neither given or recieved unauthorized help for this assignment
# Franklin Pippin

import sys
import os 
import socket


#----------GLOBALS------------

mailFromCmdPass = False
mailFromReversePath = ""
rcptToCmdPass = False
rcptToCmdCount = 0
rcptToForwardPath = []
dataCmdPass = False
dataMessage = ""
dotHit = False
handshakingPass = False


#---------Helper and Parsing Functions---------

def isCRLF(char):
    return char == '\n'

def isDigit(char):
    return char in '0123456789'

def isLetterDigit(char):
    return isLetter(char) or isDigit(char)

def isLetterDigitStr(letterDigitChar):
    char = letterDigitChar
    return isLetterDigit(char)

def isName(char):
    return isLetterDigitStr(char)

def isLetter(char):
    upperCase = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    lowerCase = 'abcdefghijklmnopqrstuvwxyz'
    return char in upperCase or char in lowerCase

def isElement(char):
    return isLetter(char) or isName(char)

def isDomain(domainChar, iterator):
    global message
    global prevChar
    char = domainChar
    if not isLetter(char) and (prevChar == '@' or prevChar == "."):
        message = '501 Syntax error in parameters or arguments'
    while isElement(char): 
        prevChar = char
        char = next(iterator)
    if char == '.':
        char = next(iterator)
        if isLetter(char): 
            return isDomain(next(iterator), iterator) 
        else: 
            message = '501 Syntax error in parameters or arguments'
    
    return char

def isSpecial(char):
    return char in '<>()[]\.,;:@"'

def isChar(char):
    return char.isprintable() and not isSpecial(char) and not isSpace(char)

def isString(char):
    return isChar(char)

def islocalPart(localPartChar, iterator):
    char = localPartChar
    while isString(char):
        char = next(iterator)
    
    return char

def isMailbox(mailboxChar, iterator):
    global message
    char = mailboxChar
    char = islocalPart(char, iterator)
    if char == mailboxChar and message == '250 OK': 
        message = '501 Syntax error in parameters or arguments'
        return char
    if char != "@" and message == '250 OK':
        message = '501 Syntax error in parameters or arguments'
        return char    
    char = next(iterator) 
    global prevChar
    prevChar = '@'
    char = isDomain(char, iterator) 
    return char

def isPath(pathChar, iterator):
    global message
    char = pathChar 
    if char != "<":
        message = '501 Syntax error in parameters or arguments'
        
    char = next(iterator) 
    char = isMailbox(char, iterator) 

    if char != ">":
        message = '501 Syntax error in parameters or arguments'
        return char  
    
    return char

def reversePath(reversePathStr):
    global reverseIterator
    reverseIterator = iter(reversePathStr)
    char = next(reverseIterator) 
    char = isPath(char, reverseIterator) 

    return char

def parseMail(mailStr):
    return mailStr == "MAIL"

def parseFrom(fromStr):
    return fromStr == "FROM:"

def isSpace(char):
    return char == ' '

def isTab(char):
    return char == '\t' 

def whiteSpace(char):
    return (isSpace(char) or isTab(char))

def mailFromCmd(inputLine):
    global mailIterator 
    mailIterator = iter(inputLine)
    global message
    message = '250 OK'
    global reversePathStr
    reversePathStr = ""
    
    try:   
        mailString = ""
        for i in range(4):
            mailString += next(mailIterator)

        if not parseMail(mailString):
            return "500 Syntax error: command unrecognized"

        char = next(mailIterator) 
        if not whiteSpace(char):
            return "500 Syntax error: command unrecognized"
        
        char = next(mailIterator) 

        while whiteSpace(char): 
            char = next(mailIterator) 
            
        fromString = ""
        fromString += char 

        for i in range(4): 
            fromString += next(mailIterator)
        
        if not parseFrom(fromString):
            return "500 Syntax error: command unrecognized"
        
        char = next(mailIterator) 

        while whiteSpace(char): 
            char = next(mailIterator) 
        
        reversePathStr = ""
        reversePathStr += char 

        while True:
            reversePathStr += next(mailIterator)
        
    except StopIteration: 
        char = reversePath(reversePathStr) 
        if message != '250 OK':
            return message

        char = next(reverseIterator)
        while whiteSpace(char): 
            char = next(reverseIterator) 

        if not isCRLF(char) and message == '250 OK': 
            return "501 Syntax error in parameters or arguments"
        
    return message

def isForwardPath(forwardString):
    global forwardIterator
    forwardIterator = iter(forwardString)
    char = next(forwardIterator) 
    isPath(char, forwardIterator)

    return char

def parseTO(toStr):
    return toStr == "TO:"

def parseRCPT(toRCPT):
    return toRCPT == "RCPT"

def rcptTo(recipientInput):
    rcptToIterator = iter(recipientInput)
    global message
    message = "250 OK"
    global forwardPathStr
    forwardPathStr = ""
    
    try:
        rcptString = ""
        for i in range(4):
            rcptString += next(rcptToIterator)
        
        if not parseRCPT(rcptString):
            return "500 Syntax error: command unrecognized"
        
        char = next(rcptToIterator) 
        if not whiteSpace(char):
            return "500 Syntax error: command unrecognized"

        char = next(rcptToIterator)  
        while whiteSpace(char):
            char = next(rcptToIterator)
        
        toString = ""
        toString += char 

        for i in range(2):  
            toString += next(rcptToIterator)
        
        if not parseTO(toString):
            return "500 Syntax error: command unrecognized"

        char = next(rcptToIterator) 

        while whiteSpace(char): 
            char = next(rcptToIterator) 
        
        forwardPathStr = ""
        forwardPathStr += char 
        
        while True:
            forwardPathStr += next(rcptToIterator)
                
    except StopIteration:
        char = isForwardPath(forwardPathStr) 
        if message != '250 OK':
            return message

        char = next(forwardIterator)
        while whiteSpace(char): 
            char = next(forwardIterator) 

        if not isCRLF(char) and message == '250 OK': 
            return "501 Syntax error in parameters or arguments"
        
        return message
    
def parseData(dataStr):
    return dataStr == 'DATA'

def data(dataInput):
    dataIterator = iter(dataInput)
    global message
    message = '354 Start mail input; end with <CRLF>.<CRLF>'

    dataStr = ""
    for i in range(4):
        dataStr += next(dataIterator)
    
    if not parseData(dataStr): 
        return "500 Syntax error: command unrecognized"


    char = next(dataIterator)
    while whiteSpace(char): 
        char = next(dataIterator) 

    if not isCRLF(char): 
        return "501 Syntax error in parameters or arguments"
    
    return message

def determineCommandType(inputCommand):
    validCommand = "250 OK"
    paramError = "501 Syntax error in parameters or arguments"
    validData = "354 Start mail input; end with <CRLF>.<CRLF>"

    mailFromCommand = mailFromCmd(inputCommand)
    rcptToCommand = rcptTo(inputCommand)
    dataCommand = data(inputCommand)

    if mailFromCommand == validCommand or mailFromCommand == paramError:
        return 1 
    
    if rcptToCommand == validCommand or rcptToCommand == paramError:
        return 2
    
    if dataCommand == validData or dataCommand == paramError:
        return 3
    
    return 4

def isolatePath(inputPath):
    openingBracketIndex = inputPath.index("<")
    closingBracketIndex = inputPath.index(">")
    path = ""

    for i in range(openingBracketIndex + 1, closingBracketIndex):
        path += inputPath[i]

    return path

def resetMachine():
    global mailFromCmdPass
    mailFromCmdPass = False
    global mailFromReversePath
    mailFromReversePath = ""
    global rcptToCmdPass
    rcptToCmdPass = False
    global rcptToCmdCount
    rcptToCmdCount = 0
    global rcptToForwardPath
    rcptToForwardPath = []
    global dataCmdPass
    dataCmdPass = False
    global dataMessage 
    dataMessage = ""
    global dotHit
    dotHit = False

def parseHELO(line):
    global prevChar

    if '@' in line: 
        prevChar = '@'
    else:
        prevChar = "."

    heloIterator = iter(line)
    heloString = ""
    for i in range(4): 
        heloString += next(heloIterator)

    if heloString != "HELO":
        sys.stdout.write('HELO incorrect\n')
        return False
    
    char = next(heloIterator)
    while whiteSpace(char):
        char = next(heloIterator)

    sys.stdout.write(f'Char before domain {char}\n')
    char = isDomain(char, heloIterator) 
    sys.stdout.write(f'Char after domain {char}\n')

    while whiteSpace(char):
        char = next(heloIterator) 

    if not isCRLF(char) and message == '250 OK':
        sys.stdout.write('CRLF incorrect\n')
        return False
    
    return True

serverPortNumber = sys.argv[1] 
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
try:
    serverSocket.bind(('', int(serverPortNumber))) 
    serverSocket.listen() 
except socket.error as E:
    sys.stdout.write(f'Error creating welcoming socket\n')
    
while True:
    try:
        clientSocket, clientAddress = serverSocket.accept()
        server220Greeting = f"220 {socket.gethostname()}\n"
        clientSocket.send(server220Greeting.encode())
        clientHELOReply = clientSocket.recv(1024).decode()

        if clientHELOReply[:4] == "HELO":
            client_hostname, _, _ = socket.gethostbyaddr(clientAddress[0])
            serverHELOAcknowledgement = f"250 Hello {client_hostname} pleased to meet you\n"
            clientSocket.send(serverHELOAcknowledgement.encode())
            handshakingPass = True
        else:
            serverHELOAcknowledgement = "500 client HELO message invalid\n" 
            clientSocket.send(serverHELOAcknowledgement.encode())

    except socket.error as E:
        sys.stdout.write(f'Error creating in handshaking\n')
        break
    
    while handshakingPass:
        clientData = clientSocket.recv(1024)
        if not clientData:
            clientSocket.close()
            resetMachine()
            handshakingPass = False
            break

        clientMessage = clientData.decode('utf-8')

        if clientMessage == "QUIT\n":
            serverMessage = f"221 {socket.gethostname()} closing connection"
            clientSocket.send(f"{serverMessage}\n".encode())
            clientSocket.close()
            resetMachine()
            handshakingPass = False
            break
        
        if not rcptToCmdPass: 
            try:
                commandType = determineCommandType(clientMessage)

            except StopIteration:
                sys.stdout.write('Non protocol error encountered, closing connection\n')
                clientSocket.close()
                resetMachine()
                handshakingPass = False
                break
            
            if commandType == 4:
                resetMachine()
                clientSocket.send("500 Syntax error: command unrecognized\n".encode())
                continue 
            
            if not mailFromCmdPass:
                if commandType == 2 or commandType == 3:
                    clientSocket.send("503 Bad sequence of commands\n".encode())
                    continue 

                mailFromCmdMessage = mailFromCmd(clientMessage)
                clientSocket.send(f"{mailFromCmdMessage}\n".encode())

                if mailFromCmdMessage[:3] == "250":
                    mailFromCmdPass = True

                continue 

            if mailFromCmdPass and not rcptToCmdPass:
                if commandType == 1 or (commandType == 3 and rcptToCmdCount == 0):
                    clientSocket.send("503 Bad sequence of commands\n".encode())
                    resetMachine()
                    continue 
            
                if commandType == 3 and rcptToCmdCount > 0:  
                    dataCmdMessage = data(clientMessage)
                    clientSocket.send(f"{dataCmdMessage}\n".encode())

                    if dataCmdMessage[:3] == "354":
                        rcptToCmdPass = True 
                    else:
                        resetMachine()
                    continue 

                rcptToCmdMessage = rcptTo(clientMessage)
                clientSocket.send(f"{rcptToCmdMessage}\n".encode())

                if rcptToCmdMessage[:3] == '250': 
                    rcptToForwardPath.append(isolatePath(clientMessage)) 
                    rcptToCmdCount += 1
                else:
                    resetMachine() 
                continue 

        elif rcptToCmdPass and not dataCmdPass: 
            
            if clientMessage == ".\n":
                dotHit = True
                dataCmdPass = True
                clientSocket.send("250 Message accepted for delivery\n".encode())
            elif clientMessage != "":  
                dataMessage += clientMessage  
            else:
                clientSocket.send("500 Syntax error: command unrecognized\n".encode())
            
            if dataCmdPass:
                domain_set = set()
                for forwardPath in rcptToForwardPath: 
                    domainStartIndex = forwardPath.index("@") + 1
                    domain = forwardPath[domainStartIndex:]
                    domain_set.add(domain)
        
                for domain in domain_set:
                    currAbsPath = os.path.abspath(__file__) 
                    currDirName = os.path.dirname(currAbsPath) 
                    
                    directory = "forward"
                    if not os.path.exists(os.path.join(currDirName, directory)):
                        os.mkdir(os.path.join(currDirName, directory)) 

                    fileName = domain 
                    filePath = os.path.join(currDirName,directory,fileName)
                    
                    with open(filePath, 'a') as file:
                        file.write(dataMessage) 

                resetMachine() 

            continue

        if rcptToCmdPass and not dataCmdPass and not dotHit:
            clientSocket.send("501 Syntax error in parameters or arguments\n".encode())
            resetMachine()
