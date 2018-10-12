'''
	Instituto Superior Tecnico - 18/19
	Redes de Computadores
	
	Grupo 14
	38731 - Sergio Silva
	83559 - Rodrigo Lima

	---  Central Server(CS)  ---

'''

import socket
import shutil
import sys
import os, os.path, sys
import select
import argparse
import select

# Globals
CS_IP = '127.0.0.1'
CS_PORT = 58014

user = None
password = None

usercommands = ['AUT', 'DLU', 'BCK', 'RST', 'LSD', 'LSF', 'DEL']
bscommands = ['REG', 'UNR', 'LFD', 'LUR', 'DBR']

#Sockets from which we expect to read
inputs = []

#Sockets from which we expect to write
outputs = []

def userHandler(socket, addr):
  print 'USER HANDLER UP'
  print '---------------'
  tosendMessage = ''
  
  autentmsg = socket.recv(18)
  autentmsg = autentmsg.split()
  
  if autentmsg[0] == 'AUT' and len(autentmsg[1]) == 5 and len(autentmsg[2]) == 8: #DONE
    if not os.path.isfile('./user_' + autentmsg[1] + '.txt'): # Se nao existir, regista
      user = autentmsg[1]
      password = autentmsg[2]
      f = open('user_' + user + '.txt', 'w')
      f.write(password)
      os.makedirs(os.path.expanduser('./user_' + user))
      f.flush()
      f.close()
      tosendMessage = 'AUR NEW\n'
      socket.send(tosendMessage)
    else: # Ja existe
      f = open('user_' + autentmsg[1] + '.txt', 'r')
      filepass = f.read()
      if filepass == autentmsg[2]:
	user = autentmsg[1]
	password = autentmsg[2]
	tosendMessage = 'AUR OK\n'
	socket.send(tosendMessage)
      else:
	tosendMessage = 'AUR NOK\n'
	socket.send(tosendMessage)
	socket.close()
  else:
    print 'ERR\n'
    sys.exit(0)
  
  command = socket.recv(1024)
  print 'COMMAND: '
  print command
  print '----------'
  if command == '\n': #So fez login
    socket.close()
  else:
    command = command.split()
    
    if command[0] in usercommands:
      if command[0] == 'DLU':
	if len(os.listdir('./user_' + user)) == 0:
	  tosendMessage = 'DLR OK\n'
	  os.remove('./user_' + user + '.txt')
	  shutil.rmtree('./user_' + user)
	  socket.send(tosendMessage)
	  socket.close()
	else:
	  tosendMessage = 'DLR NOK\n'
	  socket.send(tosendMessage)
	  socket.close()
	  
      elif command[0] == 'BCK': # TO DO
	print 'BCK'

      elif command[0] == 'RST': # TO DO
	print 'RST'

      elif command[0] == 'LSD': # TO DO
	listd = ''
	dirs = os.listdir('./user ' + user)
	n = len(os.listdir('./user_' + user + '.txt'))
	for directory in dirs:
	  listd += ' ' + directory
	  
	tosendMessage = 'LDR ' + n + listd  + '\n'
	socket.send(tosendMessage)
	socket.close()

      elif command[0] == 'LSF': # TO DO
	print 'LSF'

      elif command[0] == 'DEL': # TO DO
	print 'DEL'


def bsHandler():
  print 'BS HANDLER'


def servicetcp(s):
  user_socket, addr = s.accept()
  print 'vim aqui para aceitar a ligacao'
  
  pid = os.fork()
  if pid == 0:
    #Processo filho
    userHandler(user_socket, addr)
    sys.exit()
  elif pid == -1:
    print 'fork() ERROR'
    sys.exit()
  
def serviceudp(s):
  print 'UDP SERVICE'
  bsHandler()

'''
MAIN
'''

#Parsing of arguments
parser = argparse.ArgumentParser()

parser.add_argument('-p', help='Central Server port', type=int)

try:
  args = parser.parse_args()

except:
  print "FORMAT_ERROR: Wrong execute format."
  print "SOLUTION_EXAMPLE: python cs.py -p 58014"
  print "CENTRAL SERVER SHUTTING DOWN"
  sys.exit(0)

if args.p:
  CS_PORT = args.p

print 'PORT: ' + str(CS_PORT)
print 'IP: ' + str(CS_IP)

ADRESS = (CS_IP, int(CS_PORT)) #testas se funciona sem int()
print ADRESS

#Create and start TCP socket to listen to users
serverTCP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverTCP.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
serverTCP.bind(ADRESS)
serverTCP.listen(5)
  
#Create and start UDP socket for BS register
serverUDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serverUDP.bind(ADRESS)

#Guardar os respetivos sockets na lista de sockets input
inputs.append(serverTCP)
inputs.append(serverUDP)

while True:
  
  print 'Cheguei ao select'
  readable, writable, exceptional = select.select(inputs, outputs, inputs)
  print 'Seleccionei canal do select'
  
  for s in readable:
    if s == serverTCP:
      servicetcp(s)
    elif s == serverUDP:
      serviceudp(s)
    else:
      print 'NOT RECOGNIZED SOCKET'