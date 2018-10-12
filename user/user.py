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
import time

#GLobals
s = None

loginFlag = 0 #if 0, no login was done, it means no TCP connection open

#CS_IP = '127.0.0.1'
CS_IP = socket.gethostbyname("tejo.tecnico.ulisboa.pt")
CS_PORT = 58011

user = None
password = None

commands = ['login', 'deluser', 'backup', 'restore', 'dirlist', 'filelist', 'delete', 'logout', 'exit']

def login(user, password):
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  server_adress = (CS_IP, CS_PORT)
  print server_adress
  s.connect(server_adress)
  s.send('AUT ' + user + ' ' + password + '\n')
  print 'SENT LOGIN'
  code = s.recv(4)
  print code
  
  if code == 'AUR ':
    status = s.recv(3)
    
    if status == 'NEW':
      print 'A NEW USER AS BEEN REGISTERED'
    elif status == 'NOK':
      print 'WRONG USER PASSWORD'
    else:
      print 'USER ' + user + ' AUTENTICATED'
      
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
	print "SOLUTION_EXAMPLE: python user.py -p 58011 -n tejo.tecnico.ulisboa.pt"
	print "USER APPLICATION SHUTTING DOWN"
	sys.exit(0)

if args.p:
	CS_PORT = args.p
	print CS_PORT

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
	
    elif cmd[0] == 'deluser':
      message = 'DLU\n'
      s = login(user, password)
      s.send(message)
      
      csAnswer = s.recv(1024)    
      csAnswer = csAnswer.split()
      if csAnswer[0] == 'DLR':
	if csAnswer[1] == 'OK':
	  print 'USER DELETED WITH SUCCESS'
	elif csAnswer[1] == 'NOK':
	  print 'USER STILL HAS INFORMATION STORED. CANNOT BE DELETED'
      else:
	print 'USER REMOVAL HAS FAILED'
	sys.exit()

      s.close()
      
    elif cmd[0] == 'backup': #KINDA DONE
      s = login(user, password)
      backup_dir = cmd[1]
      
      files_description = ''
      filelist = os.listdir(backup_dir)
      for f in filelist:
	files_description += ' ' + f
	files_description += ' ' + time.strftime('%d.%m.%Y %H:%M:%S', time.gmtime(os.path.getmtime(backup_dir+'/'+f)))
	files_description += ' ' + str(os.path.getsize(backup_dir+'/'+f))
	n += 1
      
      n = str(n)
      message = 'BCK ' + backup_dir + ' ' + n + files_description + '\n'
      print 'BCK MESSAGE TO SEND:'
      print message
      print '-----------'
      
      s.send(message)
      
      try:
	a = ''
	csAnswer = ''
	c = s.recv(1)
	
	while c != '\n':
	  csAnswer += c
	  c = s.recv(1)
	  
      except socket.error:
	print 'Error receiving the BCK response'
      
      print csAnswer
      s.close()
      
      csAnswer = csAnswer.split()
      
      if csAnswer[0] == 'BKR':
	if csAnswer[1] == 'EOF':
	  print 'BCK request cannot be answered (EOF received)'
	elif csAnswer[1] == 'ERR':
	  print 'BCK request not correctly formulated (ERR received)'
	else:
	  BSip = csAnswer[1]
	  BSport = csAnswer[2]
	  n = int(csAnswer[3])
	  
	  filename_position = 4 #Gets the index of the filename for each file
	  
	  bsRequestMessage = 'UPL ' + backup_dir + ' ' + str(n)
	  
	  while n != 0:
	    filename = message[filename_position]
	    filedate = message[filename_position+1]
	    filetime = message[filename_position+2]
	    filesize = message[filename_position+3]
	    
	    filename_position += 4
	    n -= 1
	    
	    bsRequestMessage += ' ' + filename + ' ' + filedate  + ' ' + filetime + ' ' +  filesize
	    
	    f = open(backup_dir + '/' + filename, 'rb')
	    filedata = f.read()
	    f.close()
	    f.flush()
	    bsRequestMessage += filedata
	  
	  bsRequestMessage += '\n'
	  
	  bs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	  bs.connect((BSip, eval(BSport)))
	  print (BSip, BSport)
	  bs.send('AUT ' + user + ' ' + password + '\n')
	  r = bs.recv(1024)
	  print r
	  
	  bs.send(bsRequestMessage)
	  try:
	    confirmation = bs.recv(7)
	  except:
	    print 'ERROR RECEIVING A CONFIRMATION FROM THE BACKUP SERVER'
	  
	  print confirmation
	  
	  b.close()
      
    elif cmd[0] == 'restore': #KINDA DONE
      restore_dir = cmd[1]
      message = 'RST ' + restore_dir + '\n'
      
      s = login(user, password)
      s.send(message)
      
      csAnswer = s.recv(1024)
      print ' RSR ANSWER:'
      print csAnswer
      print '----------'
      csAnswer = csAnswer.split()
      s.close()
      
      if csAnswer[0] == 'RSR':
	if csAnswer[1] == 'EOF':
	  print 'RST REQUEST CANNOT BE ANSWERED. NO BS AVAILABLE'
	elif csAnswer[1] == 'ERR':
	  print 'RST REQUEST NOT CORRECTLY FORMULATED'
	else:
	  BSip = csAnswer[1]
	  BSport = csAnswer[2]
	  
	  print 'BSip: ' + BSip
	  print 'BSport: ' + BSport
	  
	  bs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	  bs.connect((BSip, eval(BSport)))
	  bs.send('AUT ' + user + ' ' + password + '\n')
	  
	  bsAnswer = bs.recv(1024)
	  print 'BS AUTENTICATION ANSWER: '
	  print bsAnswer
	  print '-------'
	  
	  bsAnswer = bsAnswer.split()
	  
	  if bsAnswer[0] == 'AUR' and bsAnswer[1] == 'NOK':
	    print 'AUTENTICATION REQUEST TO BACKUP SERVER FAILED'
	  elif bsAnswer[0] == 'AUR' and bsAnswer[1] == 'OK':
	    bs.send('RSB ' + restore_dir + '\n')
	    
	    #Receiving the data from the BS Server
	    code = bs.recv(3) #Read code
	    print code
	    if code == 'RBR':
	      bs.recv(1) #Read the space
	      
	      n=''
	      a=''
	      while a != ' ':
		a = bs.recv(1)
		n += a

	      n = int(n)
	      print n
	      
	      #Starts reading the files info and data
	      for i in range(n):
		print 'FICHEIRO ' + str(i+1)
		print '------------'
		space_counter = 0 #Counts the number of spaces encountered
		bs.recv(1) #Reads the first space before file info
		while space_counter != 5:
		  #Starts parsing the file info and data
		  if space_counter == 0:
		    a = bs.recv(1) #Reads the first letter of the filename
		    filename = ''
		    while a != ' ':
		      filename += a
		      a = bs.recv(1)
		    print 'filename: ' + filename
		    
		  elif space_counter == 1:
		    a = bs.recv(1)
		    filedate = ''
		    while a != ' ':
		      filedate += a
		      a = bs.recv(1)
		    print 'filedate: ' + filedate
		    
		  elif space_counter == 2:
		    a = bs.recv(1)
		    filetime = ''
		    while a != ' ':
		      filetime += a
		      a = bs.recv(1)
		    print 'filetime: ' + filetime
		    
		  elif space_counter == 3:
		    a = bs.recv(1)
		    filesize = ''
		    while a != ' ':
		      filesize += a
		      a = bs.recv(1)
		    print 'filesize: ' + filesize
		    
		  elif space_counter == 4:
		    filedata = bs.recv(1)
		    for i in range(int(filesize)):
		      filedata += bs.recv(1)
		    print 'filedata: ' + filedata
		    if not os.path.exists('./'+restore_dir):
		      os.makedirs('./'+restore_dir)
		    try:
		      os.remove(restore_dir+'/'+filename)
		      print filename + 'has been redone'
		    except:
		      print 'Creating file: ' + filename
		    
		    f = open(restore_dir+'/'+filename, 'wb+')
		    f.write(filedata)
		    f.close()   
		    
		  space_counter += 1
		  
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
	  
	  print str(n) + ' Files Found'
	  
	  del answer[0:4]
	  
	  i = 0
	  while i < n*4:
	    print 'Filename: ' + answer[i] + ' // date: ' + answer[i+1] + ' // time: ' + answer[i+2] + ' // size: ' + answer[i+3]
	    i += 4
      
      s.close()
      
    elif cmd[0] == 'delete':
      message = 'DEL ' + cmd[1] + '\n'
      s = login(user, password)
      s.send(message)
      
      csAnswer = s.recv(7)
      csAnswer = csAnswer.split()
      
      if csAnswer[0] == 'DDR':
	if csAnswer[1] == 'OK':
	  print 'DELETE Request was successful'
	else:
	  print 'DELETE Request was not sucessful'
      else:
	print 'WRONG FORMAT RECEIVED'
      
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