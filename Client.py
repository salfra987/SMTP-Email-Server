# I have neither receive or given unauthorized aid
# Franklin Pippin

import sys
import os
import time
import socket


#---------Helper and Parsing Functions---------

def isDigit(char):
    return char in '0123456789'

def isLetter(char):
    upperCase = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    lowerCase = 'abcdefghijklmnopqrstuvwxyz'
    return char in upperCase or char in lowerCase

def parseReversePath(line):
    try:
        reversePathIterator = iter(line)
        length = len(line)
        count = 0

        char = next(reversePathIterator)  
        count += 1

        while char.isprintable() and char not in '<>()[]\.,;:@"' and char != ' ':
            char = next(reversePathIterator)
            count += 1

        if char != '@':
            return False

        prevChar = char
        char = next(reversePathIterator)
        count += 1
        dotHit = False
        while count < length:
            if not isLetter(char) and (prevChar == '@' or prevChar == "."): 
                return False
            elif char != '.' and (not isLetter(char) and not isDigit(char)): 
                return False
            else:
                if char == ".":
                    dotHit = True
                count += 1
                prevChar = char
                char = next(reversePathIterator)

        if (not isLetter(char) and not isDigit(char)): 
            return False
        
        return True
    
    except StopIteration:
        return False

def parseForwardPath(line):
    global receiver
    receiver = []
    split_line = line.split(',')
    for forward_path in split_line:
        receiver.append(forward_path.strip())

def closeSocketTerminateProgram():
    clientSocket.close()
    sys.exit()

def quit():
    try:
        clientSocket.send("QUIT\n".encode())
        serverMessage = clientSocket.recv(1024).decode()

        if serverMessage == f'221 {serverName} closing connection\n':
            closeSocketTerminateProgram()
        else:
            sys.stdout.write("server connection not closed\n") 
            closeSocketTerminateProgram()
        
        global handshakingPass
        handshakingPass = False

    except socket.error as E:
        sys.stdout.write(f'Socket Error sending QUIT message\n')
        clientSocket.close()
        sys.exit()


def resetMachine():
    global passFrom 
    passFrom = False
    global passTo
    passTo = False
    global passSubject
    passSubject = False
    global passMessage
    passMessage = False
    global sender
    sender = ""
    global receiver
    receiver = []
    global subject
    subject = ""
    global message
    message = ""
    global headerPass
    headerPass = False


#----------GLOBALS------------

passFrom = False
passTo = False
passSubject = False
passMessage = False
sender = ""
receiver = []
subject = ""
message = ""
headerPass = False
handshakingPass = False

serverName = sys.argv[1]
serverPortNumber = sys.argv[2] 


#----------Main Code for this client-----------

try:
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    clientSocket.connect((serverName, int(serverPortNumber)))  

    serverGreeting = clientSocket.recv(1024).decode()
    if serverGreeting[:3] != '220':
        sys.stdout.write(f"Host {socket.gethostname()} did not recieve proper {serverName} server greeting message\n")
        closeSocketTerminateProgram()

    clientGreetingReply = f"HELO   {socket.gethostname()} \n" 
    clientSocket.send(clientGreetingReply.encode())

    serverMessage = clientSocket.recv(1024).decode()
    if serverMessage[:3] != '250':
        sys.stdout.write(f"Host {socket.gethostname()} did not recieve proper {serverName} server HELO acknowledgement message\n")
        closeSocketTerminateProgram()

    handshakingPass = True

except socket.error as E:
    sys.stdout.write(f'Socket Error in Handshaking\n')
    clientSocket.close()
    sys.exit()
    
while handshakingPass:
    if not passFrom:
        try:
            sys.stdout.write("From:\n")
            sender = sys.stdin.readline().strip()

            if parseReversePath(sender):  
                clientSocket.send(f"MAIL FROM: <{sender}>\n".encode())
                serverMessage = clientSocket.recv(1024).decode()

                if serverMessage[:3] == '250':
                    passFrom = True
                else:
                    sys.stdout.write("Server cannot process the client sent reverse path\n")
                    quit()
            else:
                sys.stdout.write("Invalid ReversePath, please enter a valid path\n")

            continue
    
        except socket.error as E:
            sys.stdout.write(f'Socket Error in parsing reverse-path\n')
            closeSocketTerminateProgram()

    if not passTo and passFrom:
        try:
            sys.stdout.write("To:\n")
            receivers = sys.stdin.readline().strip()
            parseForwardPath(receivers)

            for fowardPath in receiver:
                if parseReversePath(fowardPath): 
                    clientSocket.send(f"RCPT TO: <{fowardPath}>\n".encode())
                    serverMessage = clientSocket.recv(1024).decode()

                    if serverMessage[:3] == '250':
                        passTo = True
                    else:
                        passTo = False 
                        sys.stdout.write("Server cannot process the client sent forward path\n")
                        resetMachine() 
                        quit()
                        break
                else:
                    sys.stdout.write("Invalid ForwardPath, please enter a valid path\n")
                    passTo = False
                    break

            continue

        except socket.error as E:
            sys.stdout.write(f'Socket Error in parsing forward-path\n')
            closeSocketTerminateProgram()

    if not passSubject and passTo:
        try:
            sys.stdout.write("Subject:\n")
            subject = sys.stdin.readline().strip()

            clientSocket.send(f"DATA\n".encode())
            serverMessage = clientSocket.recv(1024).decode()

            if serverMessage[:3] == '354':
                passSubject = True
            else:
                sys.stdout.write("Invalid DATA command\n")
                quit()

        except socket.error as E:
            sys.stdout.write(f'Socket Error in sending subject, DATA, or receiving 354 message\n')
            closeSocketTerminateProgram()
                
    if not passMessage and passSubject:
        try:
            if not headerPass:
                sys.stdout.write("Message:\n")
                clientSocket.send(f"From: <{sender}>\n".encode())
                time.sleep(0.1) 

                receivers_string = ', '.join(f'<{receiverPath}>' for receiverPath in receiver)
                clientSocket.send(f"To: {receivers_string}\n".encode()) 
                time.sleep(0.1) 

                clientSocket.send(f"Subject: {subject}\n".encode())
                time.sleep(0.1) 

                clientSocket.send("\n".encode())                                
                time.sleep(0.1) 
                headerPass = True
            
            messageLine = sys.stdin.readline()
            clientSocket.send(f"{messageLine}".encode('utf-8'))
            time.sleep(0.1)

            if messageLine == ".\n":
                serverMessage = clientSocket.recv(1024).decode()
                if serverMessage[:3] == '250':
                    passMessage = True
                else:
                    sys.stdout.write("Server cannot process the client sent message\n")
                    sys.stdout.write(f"{serverMessage}\n")
                    quit()
            continue

        except socket.error as E:
            sys.stdout.write(f'Socket Error in creating message\n')
            closeSocketTerminateProgram()

    if passMessage:
        quit()