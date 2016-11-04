#!/usr/bin/python3.5
# _*_ coding: utf-8 _*_
# File Name: node.py
# mail: wenshizhang555@hoxmail.com
# Created Time: Thu 27 Oct 2016 11:11:28 AM CST
# Description:
#########################################################################
import	os
import	sys
import	tempfile
import	envir
import	utillib

from StringIO import StringIO
from crmsh import config

class node:
	SSH_PASSWD = ''
	WE = ''
	WORKDIR = ''
	THIS_IS_NODE = ''

	def mktemp(self):
		tmpdir = tempfile.mkdtemp()
		return tmpdir

	def get_crm_daemon_dir(self):
		'''
		Get envir.CRM_DARMON_DIR
		'''
		libdir = utillib.dirname(envir.HA_BIN)
		for p in ['/pacemaker','/heartbeat']:
			if os.access(libdir+p+'/crmd',os.X_OK):
				utillib.debug("setting CRM_DAEMON_DIR to"+libdir+p)
				envir.CRM_DAEMON_DIR = libdir+p
				return 0

		return 1

	def get_crm_daemon_dir2(self):
		'''
		Get_crm_daemon_dir function failed
		'''
		for p in ['/usr','/usr/local','/opt']:
			for d in ['libexec','lib64','lib']:
				for d2 in ['pacemaker','heartbeat']:
					if os.access(p+'/'+d+'/'+d2+'/crmd',os.X_OK):
						utillib.debug("setting CRM_DAEMON_CRM to"+p+'/'+d+'/'+d2+'/crmd')
						envir.CRM_DAEMON_DIR = p+'/'+d+'/'+d2+'/crmd'
						break

	def get_pe_state_dir(self):
		'''
		Get PE_STATE_DIR from crmsh/config/path.pe_state_dir
		'''
		envir.PE_STATE_DIR = config.path.pe_state_dir
		return len(envir.PE_STATE_DIR)
	
	def get_pe_state_dir2(self):
		'''
		Failed to get PE_STATE_DIR from crmsh
		'''
		localstatedir = utillib.dirname(envir.HA_VARLIB)
		found = utillib.find_dir("pengine","/var/lib")
		files = os.listdir(found)
		for i in files:
			if i.find(".last") != -1:
				lastf = os.path.join(found,i)

		if os.path.isfile(lastf):
			envir.PE_STATE_DIR = utillib.dirname(lastf)

		else:
			for p in ['pacemaker/pengine','pengine','heartbeat/pengine']:
				if os.path.isdir(localstatedir+'/'+p):
					utillib.debug("setting PE_STATE_DIR to "+localstatedir+'/'+p)
					envir.PE_STATE_DIR = localstatedir+'/'+p
					break

	def get_cib_dir(self):
		'''
		Get CIB_DIR from crmsh/config.path.crm_config
		'''	
		envir.CIB_DIR = config.path.crm_config
		return len(envir.CIB_DIR)
	
	def get_cib_dir2(self):
		'''
		Failed to get CIB_DIR from crmsh
		HA_VARKIB is nornally set to {localstatedir}/heartbeat
		'''
		localstatedir = utillib.dirname(envir.HA_VARLIB)
		
		for p in ['pacemaker/cib','heartbeat/crm']:
			if os.path.isfile(localstatedir+'/'+p+'/cib.xml'):
				utillib.debug("setting CIB_DIR to localstatedir+'/'+p")
				envir.CIB_DIR = localstatedir+'/'+p
				break

	def echo_ptest_tool(self):
		ptest_progs = ['crm_simulate','ptest']

		for f in ptest_progs:
			if utillib.which(f):
				break


	def compabitility_pcmk(self):				
		if self.get_crm_daemon_dir():				#have not tested carefully
			self.get_crm_daemon_dir2()

		if not len(envir.CRM_DAEMON_DIR):
			utillib.fatal("cannot find pacemaker daemon directory!")

		if self.get_pe_state_dir():
			self.get_pe_state_dir2()

		if self.get_cib_dir():
			self.get_cib_dir2()

		utillib.debug("setting PCMK_LIB to `dirname $CIB_DIR`")
		envir.PCMK_LIB = utillib.dirname(envir.CIB_DIR)

		PTEST = self.echo_ptest_tool()

	def get_cluster_type(self):
		'''
		User do not input cluster type 
		We figure out it with ourselves
		'''
		if utillib.ps_grep("corosync"):
			if not os.path.isfile('/etc/corosync/corosync.conf') or os.path.isfile(envir.HA_CF):
				utillib.debug("this is Heartbeat cluster stack")
				envir.USER_CLUSTER_TYPE = 'heartbeat'
			else:
				utillib.debug("this is Corosync cluster stack")
				envir.USER_CLUSTER_TYPE = 'corosync'

		else:
			utillib.debug("this is Corosync cluster stack")
			envir.USER_CLUSTER_TYPE = 'corosync'

	def cluster_type(self):
		'''
		Get clustetr type 
		'''
		if not len(envir.USER_CLUSTER_TYPE):
			self.get_cluster_type()

		self.get_another_dirs()
			

	def get_another_dirs(self):
		'''
		Get some dirs
		'''

		#first get CORE_DIRS and PACKAGES
		if envir.HA_VARLIB != envir.PCMK_LIB:
			envir.CORE_DIRS.append(envir.HA_VARLIB+"/cores")
			envir.CORE_DIRS.append(envir.PCMK_LIB+'/cores')
		else:
			envir.CORE_DIRS.append(envir.HA_VARLIB+'/cores')

		packages = 'pacemaker libpacemaker3 pacemaker-pygui pacemaker-pymgmt pymgmt-client openais libopenais2 libopenais3 corosync libcorosync4 resource-agents cluster-glue libglue2 ldirectord libqb0 heartbeat heartbeat-common heartbeat-resources libheartbeat2 booth ocfs2-tools ocfs2-tools-o2cb ocfs2console ocfs2-kmp-default ocfs2-kmp-pae ocfs2-kmp-xen ocfs2-kmp-debug ocfs2-kmp-trace drbd drbd-kmp-xen drbd-kmp-pae drbd-kmp-default drbd-kmp-debug drbd-kmp-trace drbd-heartbeat drbd-pacemaker drbd-utils drbd-bash-completion drbd-xen lvm2 lvm2-clvm cmirrord libdlm libdlm2 libdlm3 hawk ruby lighttpd kernel-default kernel-pae kernel-xen glibc'
		envir.PACKAGES = packages.split(" ")

		if envir.USER_CLUSTER_TYPE == 'corosync':
			envir.CONF = '/etc/corosync/corosync.conf'
			envir.CORE_DIRS.append('/var/lib/corosync')
			envir.CF_SUPPORT = envir.HA_NOARCHBIN+'/openais_conf_support.sh'
			envir.MEMBERSHIP_TOOL_OPTS = ''

		else:
			envir.CONF = envir.HA_CF
			envir.CF_SUPPORT = envir.HA_NOARCHBIN+'/ha_cf_support.sh'
			envir.MEMBERSHIP_TOOL_OPTS = '-H'

		envir.B_CONF = utillib.basename(envir.CONF)
		
		if os.path.isfile(envir.CF_SUPPORT):
			os.system('. '+envir.CF_SUPPORT)
		else:
			utillib.fatal('no stack specific support:'+envir.CF_SUPPORT)
	
	def get_log_var(self):
		'''
		Get log variable
		'''
		if len(envir.HA_LOGFACILITY):
			envir.HA_LOGFACILITY = envir.DEFAULT_HA_LOGDACILITY
			envir.HA_DEBUGLEVEL = 'info'
			cfdebug = ha_cf_support.getcfvar('debug')

	def high_debug_level1(self):
		pass


	def conf(self):
		pass

	def check_this_is_node(self):
		pass

	def getlog(self):
		pass

	def mktar(self):
		pass



