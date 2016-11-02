#!/usr/bin/python3.5
# _*_ coding: utf-8 _*_
# File Name: envir.py
# mail: wenshizhang555@hoxmail.com
# Created Time: Thu 27 Oct 2016 02:00:16 PM CST
# Description:
#########################################################################
import os
import datetime
import sys
import socket
import re

from crmsh	import utils

#unix stamptime form
FROM_TIME = 0
TO_TIME = 0

#log time form
FROM_T = ''
TO_T = ''
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
SANITIZE = []
DO_SANITIZE = 0
SKIP_LVL = 0
LOG_PATTERNS = []
NO_SSH = 0
NO_DESCRIPTION = 0
FORCE_TO_REMOVE = 0
EXTRA_LOGS = ['/var/log/messages','/var/log/pacemaker.log']
PCMK_LOG = "/var/log/pacemaker.log"
USER_CLUSTER_TYPE = ''
VERBOSITY = 0
COMPRESS = 1
SSH_PASSWD_NODES = ''
TRY_SSH = ['root','hacluster']

#the goods
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

#daemon directories
CRM_DAEMON_DIR = ''
PE_STATE_DIR = ''


#from ocf-directories
HA_BIN = ''
HA_CF = ''

