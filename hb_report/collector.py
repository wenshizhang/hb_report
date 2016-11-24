#!/usr/bin/python3.5

import	os
import	envir
import	sys
import	socket
import	utillib
import subprocess

from node import node

class collector(node):

	def debug_info(self):
		if(envir.VERBOSITY > 1):
			utillib.info("high debug level, please read debug.out")

	def sys_info(self,filename):
		'''
		create file WORKDIR/sysinfo.txt
		'''
		f = open(filename,'w')
		support = __import__(self.import_support())
		cluster_version = support.cluster_info()
		f.write(cluster_version)

		hbrp_ver = utillib.do_command([envir.HA_NOARCHBIN+'/hb_report','-V'])
		f.write(hbrp_ver)

		rsag_ver = utillib.do_grep_file('/usr/lib/ocf/lib/heartbeat/ocf-shellfuncs','Build version:')
		rsag_ver = 'resource-agents: '+rsag_ver
		f.write(rsag_ver)

		crm_version = utillib.crm_info()
		f.write(crm_version)

		booth_info = utillib.do_command(['booth','--version'])
		f.write(booth_info)
		
		pkg_info = utillib.pkg_version()
		f.write(pkg_info)
		
		print envir.SKIP_LVL
		if envir.SKIP_LVL >= 1:
			utillib.verify_packages()


	def sys_stats(self):
		pass

	def getconfig(self):
		pass

	def collect_info(self):
		self.sys_info(os.path.join(self.WORKDIR,envir.SYSINFO_F))
		self.sys_stats()

	def return_result(self):
		pass


def run(master_flag):
	sla = collector()

	#if this is master node, then flag THIS_IS_NDOE is 1, else case it is 0
	sla.THIS_IS_NODE = master_flag
	
	#who am i
	sla.WE = socket.gethostname()

	utillib.parse_xml()
	
	#get WORKDIR
	sla.WORKDIR = sla.mktemp(sla.WE)
	sla.WORKDIR = sla.WORKDIR+"/"+sla.WE
	sla.compabitility_pcmk()
	sla.cluster_type()
	support = __import__(sla.import_support())

	support.get_log_var()
	utillib.debug('log setting :facility = '+envir.HA_LOGFACILITY+' logfile = '+envir.HA_LOGFILE+' debug file = '+envir.HA_DEBUGFILE)
	

	#In order to avoid master node delete envirenv file before scp it to another node
	#Then master node donot need to delete here, it will be deleted before master node end of run
	try:
		if not sla.THIS_IS_NODE:
			if not utillib.do_rm(sla.WE,os.path.join(envir.XML_PATH,envir.XML_NAME)):
				raise IOError('NO Such file or directory')
	except IOError as msg:
		print msg
		sys.exit(1)

	sla.collect_info()

#run()
#
