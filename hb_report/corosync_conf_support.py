import os
import sys
import envir
import utillib


def getcfvar(param):
	'''
	function getcfvar parameter need to be list 
	because some place call this function and give two parameters
	and function need to check the number of parameters and to do some different things
	'''
	LOG = False
	lis = []
	if not os.path.isfile(envir.CONF):
		return
	f = open(envir.CONF,'r')
	for line in f:
		if line.startswith('#'):
			continue
		if line.find(param) != -1:
			line = line.replace(param+':','')
			line = line.replace('\t','')
			line = line.replace('\n','')
			return line

def get_coro_logvars():
	if iscfvartrue('to_file'):
		envir.HA_LOGFILE = getcfvar('logfile')
		if not len(envir.HA_LOGFILE):
			envir.HA_LOGFILE = 'syslog'
		envir.HA_DEBUGFILE = envir.HA_LOGFILE
	elif iscfvartrue('to_syslog'):
		envir.HA_LOGFACILITY = getcfvar('syslog_facility')
		if not len(envir.HA_LOGFACILITY):
			envir.HA_LOGFACILITY = 'daemon'

def get_log_var():
	'''
	Get log variable
	'''
	if not len(envir.HA_LOGFACILITY):
		envir.HA_LOGFACILITY = envir.DEFAULT_HA_LOGFACILITY
		envir.HA_DEBUGLEVEL = 'info'
	if iscfvartrue('debug'):
		HA_LOGDEVEL = 'debug'

	if  uselogd():
		if not  os.path.isfile(envir.LOGD_CF):
			#no configurations: use default
			return 
		else:
			utillib.debug('reading log settings from '+envir.LOGD_CF)
			utillib.get_logd_logvars()  #TODO
	else:
		utillib.debug('reading log setting from '+envir.CONF)
		get_coro_logvars()


def iscfvartrue(param):
	result = getcfvar(param)

	if result == 'true' or result == 'y' or result == 'on' or result == '1':
		return True
	return False

def uselogd():

	if iscfvartrue('use_logd'):
		return True

	return False

