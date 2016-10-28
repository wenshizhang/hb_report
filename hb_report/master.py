#!/usr/bin/python3.5
# _*_ coding: utf-8 _*_
# File Name: get_second.py
# mail: wenshizhang555@hoxmail.com
# Created Time: Wed 26 Oct 2016 11:28:22 AM CST
# Description:
#########################################################################
import	datetime
import	sys
import	getopt

from crmsh	import logtime
from crmsh	import utils
from crmsh	import logparser
from envir	import envir
from node	import node

class master(node):
	SUDO = ''
	LOCAL_SUDO = ''
	ENVIRONMENT = envir
	COLLECTOR_PIDS =[]

	def usage(msg = ''):
		print '''
usage: report -f {time|"cts:"testnum} [-t time]
       [-u user] [-X ssh-options] [-l file] [-n nodes] [-E files]
       [-p patt] [-L patt] [-e prog] [-MSDZAQVsvhd] [dest]

	-f time: time to start from or a CTS test number
	-t time: time to finish at (dflt: now)
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
	-A     : this is an OpenAIS cluster
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

	def __init__(self,envir):
		self.ENVIRONMRNT = envir

	def analyzed_argvment(self,argv):
		opt,argv = getopt.getopt(sys.argv[1:],"dMQASZVvhDC:f:t:n:l:E:e")
		print opt
		print argv
		self.usage()

	def mktemp(self,s):
		pass

	def is_node(self):
		pass

	def find_ssh_user(self):
		pass

	def find_sudo(self):
		pass

	def change_time(self):
		pass

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




def run():
	'''
	This method do most of the job that master node should do
	'''
	env = envir()
	mtr = master(env)
	mtr.analyzed_argvment(sys.argv)


#run('-f 3:00 -t 4:00 -n "shiwen1 shiwen2" report')
run()

