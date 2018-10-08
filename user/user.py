'''

	Instituto Superior Técnico - 18/19

	Redes de Computadores

	Grupo 14
	38731 - Sergio Silva
    83559 - Rodrigo Lima

	---  User Application  ---

'''

import socket
import sys
import signal
import os, os.path

CS_IP = socket.gethostbyname("tejo.ist.utl.pt")
CS_PORT = 58011

BUFFER_SIZE = 1024

# Globals
commands = ['login', 'deluser', 'backup', 'restore', 'dirlist', 'filelist', 'delete', 'log', 'exit']

def userCommandHandler(cmd):

	'''
	Method to handle the user commands.

	'''

	if cmd[0] in commands:

		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.connect(adress)
		message = ''

		if(cmd[0] == 'login'):
			if (len(cmd[1])==5 && len(cmd[2])==8):
				message = 'AUT ' + cmd[1] + '' + cmd[2] + '\n'
				s.send(message)

				csResponseHandler()

		elif(cmd[0] == 'deluser'):
			message = 'DLU\n'
			s.send(message)

			csResponseHandler()
		
		elif(cmd[0] == 'backup'):
			message = 'BCK ' + cmd[1]
			s.send(message)

			csResponseHandler()
		
		elif(cmd[0] == 'restore'):
			message = 'RST ' + cmd[1] + '\n'
			s.send(message)

			csResponseHandler()

		elif(cmd[0] == 'dirlist'):
			message = 'LSD\n'
			s.send(message)

			csResponseHandler()

		elif(cmd[0] == 'filelist'):
			message = 'LSF ' + cmd[1] + '\n'
			s.send(message)

			csResponseHandler()

		elif(cmd[0] == 'delete'):
			message = 'DEL ' + cmd[1] + '\n'
			s.send(message)

			csResponseHandler()

		elif(cmd[0] == 'log'):
			if (cmd[1] == 'out\n'):

		elif(cmd[0] == 'exit'):
			s.close()
			sys.exit("System down!")
	else:
		print 'Command not found. Check the input.\n'



def csResponseHandler(socket, BUFFER_SIZE):

	'''
	Method to handle the response from the Central Server

	'''

	sizeRead = 0
	answer = ''

	code = socket.recv(4) # codigo da mensagem de resposta do CS

	if(code == 'AUR '):
		#Read the status
		status = socket.recv(3)

		if(status == 'NEW'):
			print 'A NEW USER AS BEEN REGISTERED\n'

		elif(status == 'NOK'):
			print 'WRONG USER PASSWORD\n'

		else:	#OK case
			print 'AUTENTICATION WAS SUCCESSFULL\n'

	elif(code == 'DLR '):
		#Read the status
		status = socket.recv(3)

		if(status == 'NOK'):
			print 'USER STILL HAS INFORMATION STORED\n'

		else:	#OK case
			print 'USER WAS REMOVED WITH SUCCESS\n'

	elif(code == 'BKR '):
		#COMPLEXO

	elif(code == 'RSR '):


	elif(code == 'LDR '):
		#Receives the N
		n = socket.recv(1)

		if(n==0):
			print 'LSD REQUEST WAS UNSUCCESSFULL\n'
		else:

	elif(code == 'LFD '):

	elif(code == 'DDR '):
		#Read the status
		status = socket.recv(3)

		if(status == 'NOK'):
			print 'USER STILL HAS INFORMATION STORED\n'

		else:	#OK case
			print 'DEL WAS SUCCESSFULL\n'
	else:
		print'ERR\n'


'''
Main
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

host = socket.gethostname()
port = 58014

if args.p:
	port = args.p

if args.n:
	host = args.n

adress = (host, port)

# Input parsing
while True:
	cmd = raw_input("Command> ")
	cmd = cmd.split()
	userCommandHandler(cmd)