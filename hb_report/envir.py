#!/usr/bin/python3.5
# _*_ coding: utf-8 _*_
# File Name: envir.py
# mail: wenshizhang555@hoxmail.com
# Created Time: Thu 27 Oct 2016 02:00:16 PM CST
# Description:
#########################################################################
import os


class envir:
	FROM_TIME = ''
	TO_TIME = ''
	NODE_SOURCE = ''
	USER_NODES = ''
	SSH_USER = ''
	SSH_OPTS = ''
	DEST = ''
	HA_LOG = ''
	EDITOR = ''
	SANITIZE = ''
	DO_SANITIZE = ''
	SKIP_LVL = ''
	LOG_PATTERNS = ''
	NO_SSH = ''
	NO_DESCRIPTION = ''
	FORCE_TO_REMOVE = ''
	EXTRA_LOGS = ''
	USER_CLUSTER_TYPE = ''
	VERBOSITY = ''
	COMPRESS = ''
	SSH_PASSWD_NODES = ''

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
	CONFIGURATIONS="/etc/drbd.conf /etc/drbd.d /etc/booth/booth.conf"


