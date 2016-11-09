import os
import datetime
import sys
import socket
import re
import envir
import time
import StringIO

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
	if path.endswith("/"):
		path = path[1:len(path)-1]

	index = path.rfind("/")
	dirname = path[0:index]
	
	return dirname

def basename(path):
	if path.endswith("/"):
		path = path[1:len(path)-1]
	
	index = path.rfind("/")
	basename = path[index+1:]
	
	return basename


def get_ocf_directories():
	'''
	Get some critical variable that store at osc-directories 
	'''
	f = open("/usr/lib/ocf/lib/heartbeat/ocf-directories","r");
	line = f.readline()
	while len(line) >0:
		if line.find("HA_DIR:=") != -1:
			envir.HA_DIR = get_value(line,"HA_DIR")
		
		if line.find("HA_CF:=") != -1:
			envir.HA_CF = get_value(line,"HA_CF")
		
		if line.find("HA_VARLIB:=") != -1:
			envir.HA_VARLIB = get_value(line,"HA_VARLIB")

		if line.find("HA_BIN:=") != -1:
			envir.HA_BIN = get_value(line,"HA_BIN")
		line = f.readline()

def logd_getcfvar(pattern):
	'''
	TODO
	'''
	f = open(envir.LOGD_CF)
	for line in f:
		if line.startswith('#'):
			continue
		if line.startwith(pattern):
			pass

def get_logd_logvars():
	'''
	unless logfacility is set to none, heartbeat/ha_logd are
	going to log through syslog
	TODO
	'''
	envir.HA_LOGFACILITY = logd_getcfvar('logfacility')

def find_dir(name,path):
	result = []
	for root,dirs,files in os.walk(path):
		
		if name in dirs:
				result.append(os.path.join(root,name))
	
	result_string = ''.join(result)
	return result_string


def which(command):
	'''
	Implement of command which
	'''
	path = os.getenv("PATH")
	path_list = path.split(":")
	
	for p in path_list:
		if command in os.listdir(p):
			return os.path.join(p,command)

def ps_grep_pid(pid):
	'''
	Like function ps_grep, base on pid find matches
	'''
	dirs = os.listdir('/proc')
	
	for d in dirs:
		if re.match('\d+',d):
			if d == pid:
				return False

	return True

def ps_grep(proname):
	'''
	Ps and grep, if got match then return False, otherwise return True
	'''
	dirs = os.listdir("/proc")

	for d in dirs:
		if re.match("\d+",d):
			path = os.path.join('/proc',d+'/cmdline')
			f = open(path,'r')
			msg = f.readline()
			if msg.find(proname) != -1 and msg.find('grep') == -1:
				return False
	return True

def findmsg(mark):
	syslog = '/var/log /var/logs /var/syslog /var/adm /var/log/ha /var/log/cluster /var/log/pacemaker /var/log/heartbeat /var/log/crm /var/log/corosync'
	syslogdirs = syslog.split(' ')
	favourites = 'ha-*'
	log = []
	dirname = ''

	for d in syslogdirs:
		if not os.path.isdir(d):
			continue
		subdir = os.listdir(d)
		for s in subdir:
			if s.startswith('ha-'):
				if s.find(mark) != -1:
					log.append(s)
		if len(log):
			break
		for s in subdir:
			if s.find(mark) != -1:
				log.append(s)
		if len(log):
			break
	
	if len(log):
		dirs = os.listdir(log[0])
		dirsname = ' '.join(dirs)
		debug('found HA log at '+dirname)
	else:
		debug('no HA log found in '+syslog)
	
	return dirname

def iscrmrunning():
	'''
	Test whether crm is running
	if running return True, otherwise return False
	'''
	result = 0
	#if ps and grep find the crmd then return True
	if  not ps_grep('crmd'):
		return True
	pid = os.fork()
	if not pid:
		result = os.system('crmadmin -D >/dev/null 2>&1')
		if result:
			return True
		return False
	else:
		for i in range(100):
			try:
				os.waitpid(pid,0)
			except:
				break;
			time.sleep(1)
		if not ps_grep_pid(pid):
			os.kill(pid,signal.SIGKILL)

def get_crm_nodes():
	'''
	Use crm to get all node in current cluster
	Before call this function, must ensure crm is running, otherwise will get exception
	'''
	rc = 0
	from crmsh import ui_context
	from crmsh import ui_root
	from crmsh import msg
	from crmsh import options
	ui = ui_root.Root()
	context = ui_context.Context(ui)

	if len(envir.USER_NODES):
		return rc
	try:
		oldout = sys.stdout
		sys.stdout = myout= StringIO.StringIO()

		if not context.run('node server'):
			rc = 1
		sys.stdout = oldout
		nodes = myout.getvalue()
		nodes = nodes.rstrip()
		envir.USER_NODES = nodes.split('\n')
		debug('Get CRM node list: '+' '.join(envir.USER_NODES))
	except ValueError as msg:
		rc = 1
		msg.common_err(msg)
	
	return rc


def get_nodes():
	# 1. set bu user
	if len(envir.USER_NODES):
		print envir.USER_NODES
	# 2. running cr,
	elif iscrmrunning():
		debug('querying CRM for nodes')
		get_crm_nodes()
		envit.NODE_SOURCE = 'crm'
	# 3. hostcache
	elif os.path.isfile(envir.HA_VARLIB+'/hostcache'):
		utillib.debug('reading nodes from '+envir.HA_VARLIB+'/hostcache')
		get_hostcache_node()
		envir.NODE_SOURCE = 'hostcache'
	# 4. ha.cf
	elif envir.USER_CLUSTER_TYPE == 'heartbeat':
		utillib.debug('reading node from ha.cf')
		getcfvar('node')
		envir.NODE_SOURCE = 'ha.cf'
	# 5.of the cluster's stopped, try the CIB
	elif os.path.isfile(envir.CIB_DIR+'/'+envir.CIB_F):
		utillib.debug('reading node from the archived'+envir.CIB_DIR+'/'+envir.CIB_F)
		CIB_file = os.path.join(envir.CIB_DIR,envir.CIB_F)
		get_crm_node()
		envir.NODE_SOURCE = 'crm'








