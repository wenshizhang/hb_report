#!/usr/bin/python3.5

import	os
import	envir
import	sys
import	socket
import	utillib
import	corosync_conf_support

from	node import	node

class collector(node):


	def debug_info(self):
		if(envir.VERBOSITY > 1):
			utillib.info("high debug level, please read debug.out")

	def collect_info(self):
		pass

	def return_result(self):
		pass

	def get_envir(self):
		pass
	
	def __init__(self):
		pass


def run():
	sla = collector()
	
	#who am i
	sla.WE = socket.gethostname()

	#get WORKDIR
	sla.WORKDIR = sla.mktemp()
	sla.WORKDIR = sla.WORKDIR+"/"+sla.WE
	sla.compabitility_pcmk()
	sla.cluster_type()

	if envir.USER_CLUSTER_TYPE == 'corosync':
		corosync_conf_support.get_log_var()
		utillib.debug('log setting :facility = '+envir.HA_LOGFACILITY+' logfile = '+envir.HA_LOGFILE+' debug file = '+envir.HA_DEBUGFILE)
	else:
		ha_cf_support.get_log_var()

	utillib.parse_xml()

run()

