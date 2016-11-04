#!/usr/bin/python3.5

import	os
import	envir
import	sys
import	socket
import	utillib

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

	sla.get_log_var


run()

