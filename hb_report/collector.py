#!/usr/bin/python3.5

import	os
import	envir
import	sys
import	socket
import	utillib
import	corosync_conf_support

from node import node


class collector(node):

	def debug_info(self):
		if(envir.VERBOSITY > 1):
			utillib.info("high debug level, please read debug.out")

	def sys_info():
		pass

	def sys_stats():
		pass

	def getconfig():
		pass

	def collect_info(self):
		pass

	def return_result(self):
		pass


def run(master_flag):
	sla = collector()

	#if this is master node, then flag THIS_IS_NDOE is 1, else case it is 0
	sla.THIS_IS_NODE = master_flag
	
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

	#In order to avoid master node delete envirenv file before scp it to another node
	#Then master node donot need to delete here, it will be deleted before master node end of run
	try:
		if not sla.THIS_IS_NODE:
			if not utillib.do_rm(sla.WE,os.path.join(envir.XML_PATH,envir.XML_NAME)):
				raise IOError('NO Such file or directory')
	except IOError as msg:
		print msg
		sys.exit(1)

	print sla.WE,' : ',sla.WORKDIR



#run()
#
