'''

	Instituto Superior Técnico - 18/19

	Redes de Computadores

	Grupo 14
	38731 - Sergio Silva
    83559 - Rodrigo Lima

	---  Central Server (CS)  ---

'''

import socket
import sys
import os, os.path
import re


# Globals
HOST = 
PORT = 58014

commands = ['AUT ', 'DLU ', 'LSD ', 'LSF ', 'DEL ', 'BCK ', 'RST ']

def handle_user():

	'''
	Method to handle user requests
	'''

	socket.close()

	code = socket.recv(4)

	if code in commands:
		if (code == 'AUT '): #AUR STATUS (NOK; NEW; OK)
			user = socket.recv(5)
			password = socket.recv(8)
			
			toSendCode = ''

			file with users

			checks for the user:

			if the user exists but the password is wrong:
				enviar('AUR OK')
				enviar('AUR NOK')
				enviar('AUR NEW')
			elif



		elif(code == 'DLU '):

		elif(code == 'LSD '):

		elif(code == 'LSF '):

		elif(code == 'DEL '):

		elif(code == 'BCK '):

		elif(code == 'RST '):

	else:
		print 'WRONG COMMAND RECEIVED\n'




def handle_bs():

	'''
	Method to handle backup servers (BS) operations
	'''




'''
	MAIN
'''

#Parsing of arguments
parser = argparse.ArgumentParser()

parser.add_argument('-p', help='CSport', type=int)

try:
	args = parser.parse_args()

except:
	print
	print
	print
	sys.exit(0)


#Create and start UDP socket for BS register
serverUDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

#Create and start TCP socket to listen to users
serverTCP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)




