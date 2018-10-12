'''
	Instituto Superior Tecnico - 18/19
	Redes de Computadores
	
	Grupo 14
	38731 - Sergio Silva
	83559 - Rodrigo Lima

	---  Backup Server(BS)  ---

'''

import socket
import sys
import os, os.path
import time
import signal

# Globals

BSNAME =
BSPORT = 59000

CSNAME =
CSPORT = 58014

csCommands = ['RGR', 'UAR', 'LSF', 'LSU', 'DLB']
userCommands = ['', '', '', '', '', '']

def csHandler(socketUDP): # CS HANDLER WITH UDP SOCKET
  
def userHandler(socketTCP): # USER HANDLER WITH TCP SOCKET
  
  

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
  print "FORMAT_ERROR: Wrong execute format."
  print "SOLUTION_EXAMPLE: python bs.py -p 59000 -n tejo.tecnico.ulisboa.pt -p 58014"
  print "BACKUP SERVER SHUTTING DOWN"
  
if args.b:
  BS_PORT = args.b
if args.n:
  CS_NAME = args.n
if args.p:
  CS_PORT = args.p
  
print 'BSport: ' + str(BS_PORT)
print 'CSname: ' + str(CS_NAME)
print 'CSport: ' + str(CS_PORT)

#Create the UDP Socket to establish connection with CS
serverUDP = socket.socket(socket.AF_INER, socket.SOCK_DGRAM)
serverUDP.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)


  