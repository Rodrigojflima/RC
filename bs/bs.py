'''

	Instituto Superior Técnico - 18/19

	Redes de Computadores

	Grupo 14
	38731 - Sergio Silva
    83559 - Rodrigo Lima

	---  Backup Server (BS)  ---

'''

import socket
import sys
import os, os.path
import time
import signal

# Globals

BSNAME =
CSNAME =
BSPORT = 59000
CSPORT =
MAX_LISTEN = 20



def handleCs():

	'''
	Central Server (CS) handler
	'''



def handleUser():

	'''
	User handler
	'''





'''
	MAIN
'''

#Parsing of arguments

parser = argparse.ArgumentParser()

parser.add_argument('-b', help='BSport', type=int)
parser.add_argument('-n', help='CSname')
parser.add_argument('-p', help='CSport', type=int)

try:
	args = parser.parse_args()

except:
	print
	print
	print
	sys.exit(0)


#Register WS with CS (UDP)

