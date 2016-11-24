import os
import datetime
import sys
import socket
import re
import envir
import time
import StringIO
import subprocess

import xml.etree.ElementTree as ET
from xml.dom import minidom

from crmsh	import utils


#set variables default
def setvarsanddefaults():
	'''
	do some environment variable initial 
	'''
	now = datetime.datetime.now()
	now_string = now.strftime("%Y-%m-%d %H:%M:%S.%f")
	now_t = utils.parse_to_timestamp(now_string)
	envir.UNIQUE_MSG="Mark:HB_REPORT:"+str(int(now_t))
	NOW = now

	envir.TO_TIME = utils.parse_to_timestamp(now_string)
	date = datetime.datetime.date(now).strftime("%a-%d-%m-%Y")
	envir.DEST = "hb_report-"+date
	envir.SANITIZE.append("passw.*")
	envir.SSH_OPTS = ['-o StrictHostKeyChecking=no','-o EscapeChar=none','-o ConnectTimeout=15']
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
		envir.NODE_SOURCE = 'crm'
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

def do_which(command):
	path = []
	path = os.environ['PATH'].split(':')

	for n in path:
		dirlist = os.listdir(n)
		if command in dirlist:
			return True
	
	return False

def do_greple(dirs,form):
	'''
	In dirs directoriy find file text  match form
	Like grep -l -e, return the match name when get the first match 
	'''
	files = os.listdir(dirs)
	log = ''
	
	for f in files:
		#pass directires
		if not os.path.isfile(f):			
			continue

		if f.find("ha-") != -1:
			fd = open(f,'r')
			txt = fd.readline()
			#hit the targrt
			while txt:
				if txt.find(form) != -1:
					return f
				txt = fd.readline()
			fd.close()

	for f in files:

		if not os.path.isfile(f):
			continue

		fd = open(f,'r')
		txt = fd.readline()
		#hit the targrt
		while txt:
			if txt.find(form) != -1:
				return f
			txt = fd.readline()
		fd.close()
		
	return log

def do_grep_file(files,form):
	'''
	In dirs directoriy find file text  match form
	Like grep -l -e, return the match name when get the first match 
	'''
	log = ''
		
	if not os.path.isfile(files):
		fatal(files+' is not exits')

	fd = open(files,'r')
	txt = fd.readline()
	#hit the targrt
	while txt:
		if txt.find(form) != -1:
			return txt
		txt = fd.readline()
	fd.close()

	return ''
		

def findmsg():
	'''
	Found HA Log
	'''
	dirs="/var/log /var/logs /var/syslog /var/adm /var/log/ha /var/log/cluster /var/log/pacemaker /var/log/heartbeat /var/log/crm /var/log/corosync /var/log/openais"
	syslogdirs = dirs.split()
	favourites ='ha-*'
	mark = envir.UNIQUE_MSG
	log = []

	for f in syslogdirs:
		#grep pass directries
		if not os.path.isdir(f):
			continue
		log = do_greple(f,mark)
	
	if not len(log):
		debug('no HA log found in '+dirs)
	else:
		debug('found HA log at'+' '.join(log))
	
	return log


def finf_getstampproc():
	t = 0
	l = ''
	func = ''
	trycnt = 10

	#TODO
	pass

def creat_xml():

	root = ET.Element('root')

	ET.SubElement(root,'DEST').text = envir.DEST
	ET.SubElement(root,'FROM_TIME').text = str(int(envir.FROM_TIME))
	ET.SubElement(root,'TO_TIME').text = str(int(envir.TO_TIME))
	ET.SubElement(root,'USER_NODES').text = '$'.join(envir.USER_NODES)
	ET.SubElement(root,'HA_LOG').text = envir.HA_LOG
	ET.SubElement(root,'UNIQUE_MSG').text = envir.UNIQUE_MSG
	ET.SubElement(root,'SANITIZE').text = '$'.join(envir.SANITIZE)
	ET.SubElement(root,'DO_SANITIZE').text = envir.DO_SANITIZE
	ET.SubElement(root,'SKIP_LVL').text = str(envir.SKIP_LVL)
	ET.SubElement(root,'EXTRA_LOGS').text = '$'.join(envir.EXTRA_LOGS)
	ET.SubElement(root,'PCMK_LOG').text = envir.PCMK_LOG
	ET.SubElement(root,'USER_CLUSTER_TYPE').text = envir.USER_CLUSTER_TYPE
	ET.SubElement(root,'CONF').text = envir.CONF
	ET.SubElement(root,'B_CONF').text = envir.B_CONF
	ET.SubElement(root,'PACKAGES').text = '$'.join(envir.PACKAGES)
	ET.SubElement(root,'CORE_DIRS').text = '$'.join(envir.CORE_DIRS)
	ET.SubElement(root,'VERBOSITY').text = str(envir.VERBOSITY)
	ET.SubElement(root,'XML_PATH').text = str(envir.XML_PATH)
	ET.SubElement(root,'XML_NAME').text = str(envir.XML_NAME)
	ET.SubElement(root,'HA_BIN').text = str(envir.HA_BIN)



	tree = ET.tostring(root,'UTF-8')
	tree = minidom.parseString(tree).toprettyxml(indent="\t")

	path = os.path.join(envir.XML_PATH,envir.XML_NAME)

	f = open(path,'w')
	f.write(tree)
	f.close()

#	tree = ET.ElementTree(root)
#	tree.write('envir.xml')

def parse_xml():
	'''
	Parse envir.xml file
	'''
	path= os.path.join(envir.XML_PATH,envir.XML_NAME)
	root = ET.parse(path).getroot()

	for t in root:
		if t.tag == 'DEST':
			envir.DEST = t.text
		if t.tag == 'FROM_TIME':
			envir.FROM_TIME = int(t.text )
		if t.tag == 'TO_TIME':
			envir.TO_TIME = int(t.text)
		if t.tag == 'USER_NODES':
			envir.USER_NODES = t.text.split('$')
		if t.tag == 'HA_LOG':
			envir.HA_LOG = t.text
		if t.tag == 'UNIQUE_MSG':
			envir.UNIQUE_MSG = t.text
		if t.tag == 'SANITIZE':
			envir.SANITIZE = t.text.split('$')
		if t.tag == 'DO_SANITIZE':
			envir.DO_SANIZITE = t.text
		if t.tag == 'SKIP_LVL':
			envir.SKIP_LVL = int(t.text)
		if t.tag == 'EXTRA_LOGS':
			envir.EXTRA_LOGS = t.text.split('$')
		if t.tag == 'PCMK_LOG':
			envir.PCMK_LOG = t.text
		if t.tag == 'USER_CLUSTER_TYPE':
			envir.USER_CLUSTER_TYPE = t.text
		if t.tag == 'CONF':
			envir.CONF = t.text
		if t.tag == 'B_CONF':
			envir.B_CONF = t.text
		if t.tag == 'PACKAGES':
			envir.PACKAGES = t.text.split('$')
		if t.tag == 'CORE_DIRS':
			envir.CORE_DIRS = t.text.split('$')
		if t.tag == 'VERBOSITY':
			envir.VERBOSITY = int(t.text)
		if t.tag == 'XML_NAME':
			envir.XML_NAME = t.text
		if t.tag == 'XML_PATH':
			envir.XML_PATH = t.text
		if t.tag == 'HA_BIN':
			envir.HA_BIN = t.text

#		os.remove(path)

def check_user():
	'''
	hb_report force user run as root
	so run it, the user shoule be check
	'''
	euid = os.geteuid()
	if euid:
		fatal('Please run hb_report as root!')
	
def do_rm(nodes,filepath):
	'''
	Remove file base on path absolute path filepath
	'''
	if not os.path.isfile(filepath):
		debug(nodes+': '+filepath+'is not exits')
		return False
	os.remove(filepath)
	debug(nodes+' remove file :'+filepath)
	return True

def crm_info():
	'''
	Get crmd version
	'''
	crm_pro = subprocess.Popen([envir.CRM_DAEMON_DIR+'/crmd','version'],stdout = subprocess.PIPE,stderr = subprocess.STDOUT)
	return crm_pro.communicate()[0]


def do_command(argv):
	'''
	call subprocess do 
	'''
	command = argv[0]
	if not do_which(command):
		debug(command+' is not found')
		msg = command+' : command not found'
		return msg
	comm_list = command.split()
	comm_list.extend(argv)

	com_pro = subprocess.Popen(comm_list,stdout = subprocess.PIPE,stderr = subprocess.STDOUT)

	msg = com_pro.communicate()[0]
	return msg

def pkg_ver_deb():
	argv = ['dpkg-query','-f',"${Name} ${Version}",'-W']
	argv.extend(emvir.PACKAGES)

	msg = do_command(argv)

	return msg

def pkg_ver_pkg_info():
	#TODO
	pass
def pkg_ver_pkginfo():
	#TODO
	pass

def pkg_ver_rpm():
	argv = ['rpm','-q','--qf',"%{name} %{version}-%{release} - %{distribution} %{arch}\n"]
	argv.extend(envir.PACKAGES)

	rpm_pro = subprocess.Popen(argv,stdout = subprocess.PIPE,stderr = subprocess.STDOUT)
	grep_pro = subprocess.Popen(['grep','-v',"not installed"],stdin = rpm_pro.stdout,stdout = subprocess.PIPE)

	pkg_info = grep_pro.communicate()[0]

	return pkg_info

def pkg_version():

	pkg_mgr = get_pkg_mgr()

	if not len(pkg_mgr):
		debug('pkg_mgr not found')
		return

	debug('the package manager is '+pkg_mgr)

	func = globals()['pkg_ver_'+pkg_mgr]
	pkg_info = func()

	return pkg_info

def get_pkg_mgr():
	
	if do_which('dpkg'):
		pkg_mgr = 'deb'
	elif do_which('rpm'):
		pkg_mgr = 'rpm'
	elif do_which('pkg_info'):
		pkg_mgr = 'pkg_info'
	elif do_which('pkginfo'):
		pkg_mgr ='pkginfo'
	else:
		warning('Unknown package manager!')
		return

	return pkg_mgr

def verify_rpm():

	argv = ['rpm','--verify']
	argv.extend(envir.PACKAGES)

	rpm_pro = subprocess.Popen(argv,stdout = subprocess.PIPE,stderr = subprocess.STDOUT)
#	rpm_pro.wait()
	grep_pro = subprocess.Popen(['grep','-v',"not installed"],stdin = rpm_pro.stdout,stdout = subprocess.PIPE,stderr = subprocess.STDOUT)

#	rpm_msg = grep_pro.communicate()[0]
	rpm_msg = rpm_pro.communicate()[0]
	return rpm_msg

def verify_deb():
	
	argv = ['debsums','-s']
	argv.extend(envir.PACKAGES)

	deb_info = do_command(argv)

	return deb_info

def verify_pkg_info:
	'''
	Do not need to get
	'''
	pass
def verify_pkginfo:
	'''
	Do not need to get
	'''
	pass

def verify_packages():

	pkg_mgr = get_pkg_mgr()

	if not len(pkg_mgr):
		return
	func = globals()['verify_'+pkg_mgr]
	func()






















