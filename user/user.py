'''
	Instituto Superior Tecnico - 18/19
	Redes de Computadores
	
	Grupo 14
	38731 - Sergio Silva
	83559 - Rodrigo Lima

	---  User Application  ---

'''

import socket
import sys
import signal
import os
import argparse

#GLobals
s = None

loginFlag = 0 #if 0, no login was done, it means no TCP connection open

CS_IP = socket.gethostbyname("tejo.ist.utl.pt")
CS_PORT = 58011

user = None
password = None

commands = ['login', 'deluser', 'backup', 'restore', 'dirlist', 'filelist', 'delete', 'logout', 'exit']

def login(user, password):
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  server_adress = (CS_HOST, CS_PORT)
  s.connect(server_adress)
  s.send('AUT ' + user + ' ' + password + '\n')
  code = s.recv(4)
  print  code
  
  if code == 'AUR ':
    status = s.recv(3)
    
    if status == 'NEW':
      print 'A NEW USER AS BEEN REGISTERED'
    elif status == 'NOK':
      print 'WRONG USER PASSWORD'
    else:
      print 'AUTENTICATION WAS SUCCESSFULL'
      
  return s

'''
MAIN
'''

# Parsing the compiling arguments
parser = argparse.ArgumentParser()

parser.add_argument("-n", help="CS host")
parser.add_argument("-p", help="CS port", type=int)

try:
	args = parser.parse_args()

except:
	print "FORMAT_ERROR: Wrong execute format."
	print "SOLUTION_EXAMPLE: python user.py -p 58014 -n tejo.ist.utl.pt"
	print "USER APPLICATION SHUTTING DOWN"
	sys.exit(0)

if args.p:
	CS_PORT = args.p

if args.n:
	CS_HOST = args.n

print 'PORT: ' + str(CS_PORT)
print 'HOST: ' + str(CS_HOST)

# Input parsing
while True:
  cmd = raw_input("Command> ")
  cmd = cmd.split()
  
  if cmd[0] in commands:
    message = ''
    
    if cmd[0] == 'login':
      if len(cmd[1])==5 and len(cmd[2])==8:
	user = cmd[1]
	password = cmd[2]
	loginFlag = 1
	s = login(user, password)
	
    elif cmd[0] == 'deluser': #TO DO
      message = 'DLU\n'
      s.send(message)
      
      csResponseHandler()
      
    elif cmd[0] == 'backup': #TO DO
      message = 'BCK ' + cmd[1] + '\n'
      s.send(message)
      
      csResponseHandler()
      
    elif cmd[0] == 'restore': #TO END
      message = 'RST ' + cmd[1] + '\n'
      s = login(user, password)
      s.send(message)
      
      csAnswer = s.recv(25)
      csAnswer = csAnswer.split()
      if csAnswer[0] == 'RSR':
	if csAnswer[1] == 'EOF':
	  print 'RST REQUEST CANNOT BE ANSWERED'
	elif csAnswer[1] == 'ERR':
	  print 'BCK REQUEST NOT CORRECTLY FORMULATED'
	else:
	  print 'BSip: ' + answer[1]
	  print 'BSport: ' + answer[2]
	  
	  s.close()
	  
	  '''
	  A continuar
	  '''
	  
    elif cmd[0] == 'dirlist':
      message = 'LSD\n'
      s = login(user, password)
      s.send(message)
      
      answer = ''
      a = ''
      
      while a != '\n':
	a = s.recv(1)
	answer += a
      
      answer = answer.split()
      
      if answer[0] == 'LDR':
	if answer[1] == 0:
	  print 'LSD REQUEST WAS NOT SUCESSFULL'
	else:
	  n = str(answer[1])
	  print n + ' Directories Found'
	  del answer[0:2]
	  
	  for directory in answer:
	    print 'Directoryname: ' + directory
	  
	  
      s.close()
      
    elif cmd[0] == 'filelist':
      message = 'LSF ' + cmd[1] + '\n'
      s = login(user, password)
      s.send(message)
      
      answer = ''
      a = ''
      
      while a != '\n':
	a = s.recv(1)
	answer += a
      
      answer = answer.split()
      
      if answer[0] == 'LFD' and answer[1] == 'NOK':
	print 'LSF REQUEST CANNOT BE ANSWERED'
	
      elif answer[0] == 'LFD':
	  n = int(answer[3])
	  print 'BSip: ' + answer[1]
	  print 'BSport: ' + answer[2]
	  
	  del answer[0:4]
	  
	  i = 0
	  while i < n*4:
	    print 'Filename: ' + answer[i] + ' // date: ' + answer[i+1] + ' // time: ' + answer[i+2] + ' // size: ' + answer[i+3]
	    i += 4
      
      s.close()
      
    elif cmd[0] == 'delete': #TO DO
      message = 'DEL ' + cmd[1] + '\n'
      s.send(message)
      
    elif cmd[0] == 'logout':
      if user != None and password != None:
	print 'User ' + user + ' has been logged out'
	user = None
	password = None
      else:
	print 'NO PREVIOUS LOGGED IN USER'
      
    elif cmd[0] == 'exit':
      s.close()
      sys.exit('SYSTEM DOWN!')
  
  else:
   print 'Command not found. Check the input.'