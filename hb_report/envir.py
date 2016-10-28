#!/usr/bin/python3.5
# _*_ coding: utf-8 _*_
# File Name: envir.py
# mail: wenshizhang555@hoxmail.com
# Created Time: Thu 27 Oct 2016 02:00:16 PM CST
# Description:
#########################################################################
import os
import datetime

from crmsh	import utils
FROM_TIME = ''
TO_TIME = ''
NODE_SOURCE = ''
USER_NODES=[]
UNIQUE_MSG = ""
SSH_USER = []
SSH_OPTS = ''
DEST = ''
DESTDIR = '.'
NOW = ''
HA_LOG = ''
EDITOR = ''
SANITIZE = 'passw.*'
DO_SANITIZE = ''
SKIP_LVL = 0
LOG_PATTERNS = ''
NO_SSH = ''
NO_DESCRIPTION = '1'
FORCE_TO_REMOVE = ''
EXTRA_LOGS = ['/var/log/messages','/var/log/pacemaker.log']
PCMK_LOG = "/var/log/pacemaker.log"
USER_CLUSTER_TYPE = ''
VERBOSITY = 0
COMPRESS = '1'
SSH_PASSWD_NODES = ''
TRY_SSH = ['root','hacluster']

ANALYSIS_F='analysis.txt'
DESCRIPTION_F='description.txt'
HALOG_F='ha-log.txt'
JOURNAL_F='journal.log'
BT_F='backtraces.txt'
SYSINFO_F='sysinfo.txt'
SYSSTATS_F='sysstats.txt'
DLM_DUMP_F='dlm_dump.txt'
TIME_F='time.txt'
CRM_MON_F='crm_mon.txt'
MEMBERSHIP_F='members.txt'
HB_UUID_F='hb_uuid.txt'
HOSTCACHE='hostcache'
CRM_VERIFY_F='crm_verify.txt'
PERMISSIONS_F='permissions.txt'
CIB_F='cib.xml'
CIB_TXT_F='cib.txt'
COROSYNC_RECORDER_F='fdata.txt'
CONFIGURATIONS=['/etc/drbd.conf','/etc/drbd.d','/etc/booth/booth.conf']
def __init__(self):
	'''
	do some environment variable initial 
	'''
	now = datetime.datetime.now()
	now_string = now.strftime("%Y-%m-%d %H:%M:%S.%f")
	self.UNIQUE_MSG="Mark:HB_REPORT:"+now_string
	self.NOW = now

	TO_TIME = utils.parse_to_timestamp(now_string)
	date = datetime.datetime.date(now).strftime("%a-%d-%m-%Y")
	self.DEST = "hb_report-"+date
