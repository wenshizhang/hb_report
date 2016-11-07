# Copyright (C) 2016 Shiwen Zhang <szhang@suse.de>
# See COPYING for license information.

import	os
import	datetime
import	sys
import	getopt
import	envir
import	socket
import	utillib
import	corosync_conf_support
import	ha_cf_support

from crmsh	import logtime
from crmsh	import utils
from crmsh	import logparser
from node	import node

class master(node):
	SUDO = ''
	LOCAL_SUDO = ''
	COLLECTOR_PIDS =[]

	def version(self):
		print "crmsh: 2.2.0+git.1464769043.9e4df55"
		sys.exit

	def usage(self,msg = ''):
		print '''usage: report -f {time|"cts:"testnum} [-t time]
       [-u user] [-X ssh-options] [-l file] [-n nodes] [-E files]
       [-p patt] [-L patt] [-e prog] [-MSDZAQVsvhd] [dest]

	-f time: time to start from or a CTS test number
	-t time: time to finish at (dflt: now)
	-s	   : do sanitize
	-d     : don't compress, but leave result in a directory
	-n nodes: node names for this cluster; this option is additive
			 (use either -n "a b" or -n a -n b)
	         if you run report on the loghost or use autojoin,
	         it is highly recommended to set this option
	-u user: ssh user to access other nodes (dflt: empty, root, hacluster)
	-X ssh-options: extra ssh(1) options
	-l file: log file
	-E file: extra logs to collect; this option is additive
	         (dflt: /var/log/messages)
	-s     : sanitize the PE and CIB files
	-p patt: regular expression to match variables containing sensitive data;
	         this option is additive (dflt: "passw.*")
	-L patt: regular expression to match in log files for analysis;
	         this option is additive (dflt: $LOG_PATTERNS)
	-e prog: your favourite editor
	-Q     : don't run resource intensive operations (speed up)
	-M     : don't collect extra logs (/var/log/messages)
	-D     : don't invoke editor to write description
	-Z     : if destination directories exist, remove them instead of exiting
	         (this is default for CTS)
	-S     : single node operation; don't try to start report
	         collectors on other nodes
	-v     : increase verbosity
	-V     : print version
	dest   : report name (may include path where to store the report)
		'''
		if msg != "short":
			print '''

	. the multifile output is stored in a tarball {dest}.tar.bz2
	. the time specification is as in either Date::Parse or
	  Date::Manip, whatever you have installed; Date::Parse is
	  preferred
	. we try to figure where is the logfile; if we can't, please
	  clue us in ('-l')
	. we collect only one logfile and /var/log/messages; if you
	  have more than one logfile, then use '-E' option to supply
	  as many as you want ('-M' empties the list)

	Examples

	  report -f 2pm report_1
	  report -f "2007/9/5 12:30" -t "2007/9/5 14:00" report_2
	  report -f 1:00 -t 3:00 -l /var/log/cluster/ha-debug report_3
	  report -f "09sep07 2:00" -u hbadmin report_4
	  report -f 18:00 -p "usern.*" -p "admin.*" report_5
	  report -f cts:133 ctstest_133

	. WARNING . WARNING . WARNING . WARNING . WARNING . WARNING .

	  We won't sanitize the CIB and the peinputs files, because
	  that would make them useless when trying to reproduce the
	  PE behaviour. You may still choose to obliterate sensitive
	  information if you use the -s and -p options, but in that
	  case the support may be lacking as well. The logs and the
	  crm_mon, ccm_tool, and crm_verify output are *not* sanitized.

	  Additional system logs (/var/log/messages) are collected in
	  order to have a more complete report. If you don't want that
	  specify -M.

	  IT IS YOUR RESPONSIBILITY TO PROTECT THE DATA FROM EXPOSURE!

			'''


	def analyzed_argvment(self,argv):
		try:
			opt,arg = getopt.getopt(sys.argv[1:],"hsQSDCZMAvdf:t:n:u:X:l:e:p:L:E:")
			if(len(arg)>1):
				self.usage("short")
				sys.exit()

			if(len(arg) == 1):
				envir.DEST = arg
			for args,option in opt:
				if (args == '-f'):
					envir.FROM_TIME = self.change_to_timestamp(option)
				if (args == '-t'):
					envir.TO_TIME  = self.change_to_timestamp(option)
				if (args == '-n'):
					envir.NODE_SOURCE = 'user'
					for i in option.split(' '):
						envir.USER_NODES.append(i)
				if (args == '-h'):
					self.usage()
				if (args == '-u'):
					envir.SSH_USER.append(option)
				if (args == '-X'):
					envir.SSH_OPTS = envir.SSH_OPTS+option
				if (args == '-l'):
					envir.HA_LOG = option
				if(args == '-e'):
					envir.EDITOR = option
				if(args == '-p'):
					envir.SANITIZE.append(option)
				if(args == '-s'):
					envir.DO_SANITIZE = 1
				if(args == '-Q'):
					envir.SKIP_LVL = envir.SKIP_LVL + 1
				if(args == '-L'):
					envir.LOG_PATTERNS.append(option)
				if(args == '-S'):
					envir.NO_SSH = 1
				if(args == '-D'):
					envir.NO_DESCRIPTION = 1
				if(args == '-C'):
					pass
				if(args == '-Z'):
					envir.FORCE_REMOVE_DEST = 1
				if(args == '-M'):
					envir.EXTRA_LOGS = []
				if(args == '-E'):
					envir.EXTRA_LOGS.append(option)
#				if(args == '-A'):
#					envir.USER_CLUSTER_TYPE = 'openais'
				if(args == '-v'):
					envir.VERBOSITY = envir.VERBOSITY+1
				if(args == '-d'):
					envir.COMPRSS = 0
		except getopt.GetoptError:
			self.usage("short")
			envir.SSH_USER.append("root")
			envir.SSH_USER.append("hacluster")



	def is_node(self):
		pass

	def find_ssh_user(self):
		pass

	def find_sudo(self):
		pass

	def change_to_timestamp(self,time):
		ds = utils.parse_to_timestamp(time)
		return ds

	def collect_for_nodes(self):
		pass

	def start_collect(self):
		pass

	def analyzed(self):
		pass

	def events(self):
		pass

	def check_if_log_is_empty(self):
		pass

	def final_word(self):
		pass

	def send_envir(self):
		pass
	
	def get_cts_log(self):
		ctslog = utillib.findmsg('CTS: Stack:')



def run():
	'''
	This method do most of the job that master node should do
	'''
	utillib.setvarsanddefaults()
	utillib.get_ocf_directories()

	mtr = master()
	mtr.analyzed_argvment(sys.argv)
	
	#who am i
	mtr.WE= socket.gethostname()
	
	#get WORKDIR
	mtr.WORKDIR = mtr.mktemp()
	mtr.compabitility_pcmk()
	mtr.cluster_type()
	if not len(envir.CTS):
		if envir.USER_CLUSTER_TYPE == 'corosync':
			corosync_conf_support.get_log_var()
			utillib.debug('log setting :facility = '+envir.HA_LOGFACILITY+' logfile = '+envir.HA_LOGFILE+' debug file = '+envir.HA_DEBUGFILE)
		else:
			ha_cf_support.get_log_var()
	else:
		mtr.get_cts_log()

run()

