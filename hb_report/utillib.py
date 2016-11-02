import os
import datetime
import sys
import socket
import re
import envir

from crmsh	import utils

#set variables default
def setvarsanddefaults():
	'''
	do some environment variable initial 
	'''
	now = datetime.datetime.now()
	now_string = now.strftime("%Y-%m-%d %H:%M:%S.%f")
	envir.UNIQUE_MSG="Mark:HB_REPORT:"+now_string
	NOW = now

	envir.TO_TIME = utils.parse_to_timestamp(now_string)
	date = datetime.datetime.date(now).strftime("%a-%d-%m-%Y")
	envir.DEST = "hb_report-"+date
	envir.SANITIZE.append("passw.*")
	envir.LOG_PATTERNS.append("CRIT:")
	envir.LOG_PATTERNS.append("ERROR:")

def debug(msg):
	if (envir.VERBOSITY >0):
		print >> sys.stderr,socket.gethostname(),"DEBUG:",msg
		return 0

def fatal(msg):
	print >> sys.stderr,socket.gethostname(),"ERROR:",msg
	sys.exit(1)

def warn(msg):
	print >>sys.stderr,socket.gethostname(),"WARN:",msg

def info(msg):
	print >> sys.stderr,socket.gethostname(),"INFO:",msg

def get_value(line,key):
	'''
	Base on parameter key to search and get the value in string line
	'''
	value = line.split("=")
	value = str(value[1:])
	value = value[2:len(value)-5]
	return value

def dirname(path):
	index = path.rfind("/")

def get_ocf_directories():
	'''
	Get some critical variable that store at osc-directories 
	'''
	f = open("/usr/lib/ocf/lib/heartbeat/ocf-directories","r");
	line = f.readline()
	while len(line) >0:
		if line.find("HA_DIR:=") != -1:
			envir.HA_DIR = get_value(line,"HA_DIR")
		if line.find("HA_BIN:=") != -1:
			envir.HA_BIN = get_value(line,"HA_BIN")
		line = f.readline()
