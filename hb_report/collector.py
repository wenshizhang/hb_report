#!/usr/bin/python3.5

import	os
import	envir
import	sys
import	socket
import	utillib
import subprocess
import platform

from node import node

class collector(node):

	def debug_info(self):
		if(envir.VERBOSITY > 1):
			utillib.info("high debug level, please read debug.out")

	def sys_info(self,filename):
		'''
		create file WORKDIR/sysinfo.txt
		'''
		msg = ''
		print 'WORKDIR IS',self.WORKDIR
		f = open(filename,'w')
		support = __import__(self.import_support())
		cluster_version = support.cluster_info()
		msg = cluster_version

		hbrp_ver = utillib.do_command([envir.HA_NOARCHBIN+'/hb_report','-V'])
		msg = msg+hbrp_ver

		rsag_ver = utillib.do_grep_file('/usr/lib/ocf/lib/heartbeat/ocf-shellfuncs','Build version:')
		rsag_ver = 'resource-agents: '+rsag_ver
		msg = msg + rsag_ver

		crm_version = utillib.crm_info()
		msg = msg+crm_version

		booth_info = utillib.do_command(['booth','--version'])
		msg = msg+booth_info
		
		pkg_info = utillib.pkg_version()
		msg = msg + pkg_info
		f.write(pkg_info)
		
		if envir.SKIP_LVL >= 1:
			vrf_info = utillib.verify_packages()
			msg = msg + vrf_info

		sys_name = 'Platform: '+ platform.system()+'\n'
		msg = msg+sys_name

		knl_name = 'Kernel release: '+platform.release()+'\n'
		msg = msg+knl_name
		
		arch_name = 'Architecture: '+platform.machine()+'\n'
		msg = msg+arch_name

		if platform.system() == 'Linux':
			dist_name = utillib.distro()+'\n'
			msg = msg + dist_name
		f.write(msg)
		f.close()

	def sys_stats(self):
		
		f = open(os.path.join(self.WORKDIR,envir.SYSSTATS_F),'w')
		msg = ''

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
