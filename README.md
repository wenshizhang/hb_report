#SYNOPSIS
       hb_report -f {time|"cts:"testnum} [-t time] [-u user] [-l file] [-n nodes] [-E files] [-p patt] [-L patt] [-e prog] [-MSDCZAQVsvhd]
       [dest]

#DESCRIPTION
       The hb_report(1) is a utility to collect all information (logs, configuration files, system information, etc) relevant to Pacemaker
       (CRM) over the given period of time.

#OPTIONS
       dest
           The report name. It can also contain a path where to put the report tarball. If left out, the tarball is created in the current
           directory named "hb_report-current_date", for instance hb_report-Wed-03-Mar-2010.

       -d
           Don't create the compressed tar, but leave the result in a directory.

       -f { time | "cts:"testnum }
           The start time from which to collect logs. The time is in the format as used by the Date::Parse perl module. For cts tests, specify
           the "cts:" string followed by the test number. This option is required.

       -t time
           The end time to which to collect logs. Defaults to now.

       -n nodes
           A list of space separated hostnames (cluster members). hb_report may try to find out the set of nodes by itself, but if it runs on
           the loghost which, as it is usually the case, does not belong to the cluster, that may be difficult. Also, OpenAIS doesn't contain
           a list of nodes and if Pacemaker is not running, there is no way to find it out automatically. This option is cumulative (i.e. use
           -n "a b" or -n a -n b).

       -l file
           Log file location. If, for whatever reason, hb_report cannot find the log files, you can specify its absolute path.

       -E files
           Extra log files to collect. This option is cumulative. By default, /var/log/messages are collected along with the cluster logs.

       -M
           Don't collect extra log files, but only the file containing messages from the cluster subsystems.

       -L patt
           A list of regular expressions to match in log files for analysis. This option is additive (default: "CRIT: ERROR:").

       -p patt
           Additional patterns to match parameter name which contain sensitive information. This option is additive (default: "passw.*").

       -Q
           Quick run. Gathering some system information can be expensive. With this option, such operations are skipped and thus information
           collecting sped up. The operations considered I/O or CPU intensive: verifying installed packages content, sanitizing files for
           sensitive information, and producing dot files from PE inputs.

       -A
           This is an OpenAIS cluster. hb_report has some heuristics to find the cluster stack, but that is not always reliable. By default,
           hb_report assumes that it is run on a Heartbeat cluster.

       -u user
           The ssh user. hb_report will try to login to other nodes without specifying a user, then as "root", and finally as "hacluster". If
           you have another user for administration over ssh, please use this option.

       -X ssh-options
           Extra ssh options. These will be added to every ssh invocation. Alternatively, use $HOME/.ssh/config to setup desired ssh
           connection options.

       -S
           Single node operation. Run hb_report only on this node and don't try to start slave collectors on other members of the cluster.
           Under normal circumstances this option is not needed. Use if ssh(1) does not work to other nodes.

       -Z
           If the destination directory exist, remove it instead of exiting (this is default for CTS).

       -V
           Print the version including the last repository changeset.

       -v
           Increase verbosity. Normally used to debug unexpected behaviour.

       -h
           Show usage and some examples.

       -D (obsolete)
           Don't invoke editor to fill the description text file.

       -e prog (obsolete)
           Your favourite text editor. Defaults to $EDITOR, vim, vi, emacs, or nano, whichever is found first.

       -C (obsolete)
           Remove the destination directory once the report has been put in a tarball.

#EXAMPLES
       Last night during the backup there were several warnings encountered (logserver is the log host):

           logserver# hb_report -f 3:00 -t 4:00 -n "node1 node2" report

       collects everything from all nodes from 3am to 4am last night. The files are compressed to a tarball report.tar.bz2.

       Just found a problem during testing:

           # note the current time
           node1# date
           Fri Sep 11 18:51:40 CEST 2009
           node1# /etc/init.d/heartbeat start
           node1# nasty-command-that-breaks-things
           node1# sleep 120 #wait for the cluster to settle
           node1# hb_report -f 18:51 hb1

           # if hb_report can't figure out that this is corosync
           node1# hb_report -f 18:51 -A hb1

           # if hb_report can't figure out the cluster members
           node1# hb_report -f 18:51 -n "node1 node2" hb1

       The files are compressed to a tarball hb1.tar.bz2.

#INTERPRETING RESULTS
       The compressed tar archive is the final product of hb_report. This is one example of its content, for a CTS test case on a three node
       OpenAIS cluster:

           $ ls -RF 001-Restart

           001-Restart:
           analysis.txt     events.txt  logd.cf       s390vm13/  s390vm16/
           description.txt  ha-log.txt  openais.conf  s390vm14/

           001-Restart/s390vm13:
           STOPPED  crm_verify.txt  hb_uuid.txt  openais.conf@   sysinfo.txt
           cib.txt  dlm_dump.txt    logd.cf@     pengine/        sysstats.txt
           cib.xml  events.txt      messages     permissions.txt

           001-Restart/s390vm13/pengine:
           pe-input-738.bz2  pe-input-740.bz2  pe-warn-450.bz2
           pe-input-739.bz2  pe-warn-449.bz2   pe-warn-451.bz2

           001-Restart/s390vm14:
           STOPPED  crm_verify.txt  hb_uuid.txt  openais.conf@   sysstats.txt
           cib.txt  dlm_dump.txt    logd.cf@     permissions.txt
           cib.xml  events.txt      messages     sysinfo.txt

           001-Restart/s390vm16:
           STOPPED  crm_verify.txt  hb_uuid.txt  messages        sysinfo.txt
           cib.txt  dlm_dump.txt    hostcache    openais.conf@   sysstats.txt
           cib.xml  events.txt      logd.cf@     permissions.txt

       The top directory contains information which pertains to the cluster or event as a whole. Files with exactly the same content on all
       nodes will also be at the top, with per-node links created (as it is in this example the case with openais.conf and logd.cf).

       The cluster log files are named ha-log.txt regardless of the actual log file name on the system. If it is found on the loghost, then it
       is placed in the top directory. If not, the top directory ha-log.txt contains all nodes logs merged and sorted by time. Files named
       messages are excerpts of /var/log/messages from nodes.

       Most files are copied verbatim or they contain output of a command. For instance, cib.xml is a copy of the CIB found in
       /var/lib/heartbeat/crm/cib.xml. crm_verify.txt is output of the crm_verify(8) program.

       Some files are result of a more involved processing:

       analysis.txt
           A set of log messages matching user defined patterns (may be provided with the -L option).

       events.txt
           A set of log messages matching event patterns. It should provide information about major cluster motions without unnecessary
           details. These patterns are devised by the cluster experts. Currently, the patterns cover membership and quorum changes, resource
           starts and stops, fencing (stonith) actions, and cluster starts and stops. events.txt is always generated for each node. In case
           the central cluster log was found, also combined for all nodes.

       permissions.txt
           One of the more common problem causes are file and directory permissions. hb_report looks for a set of predefined directories and
           checks their permissions. Any issues are reported here.

       backtraces.txt
           gdb generated backtrace information for cores dumped within the specified period.

       sysinfo.txt
           Various release information about the platform, kernel, operating system, packages, and anything else deemed to be relevant. The
           static part of the system.

       sysstats.txt
           Output of various system commands such as ps(1), uptime(1), netstat(8), and ifconfig(8). The dynamic part of the system.

       description.txt should contain a user supplied description of the problem, but since it is very seldom used, it will be dropped from
       the future releases.

#PREREQUISITES
       ssh
           It is not strictly required, but you won't regret having a password-less ssh. It is not too difficult to setup and will save you a
           lot of time. If you can't have it, for example because your security policy does not allow such a thing, or you just prefer menial
           work, then you will have to resort to the semi-manual semi-automated report generation. See below for instructions.

           If you need to supply a password for your passphrase/login, then always use the -u option.

           For extra ssh(1) options, if you're too lazy to setup $HOME/.ssh/config, use the -X option. Do not forget to put the options in
           quotes.

       sudo
           If the ssh user (as specified with the -u option) is other than root, then hb_report uses sudo to collect the information which is
           readable only by the root user. In that case it is required to setup the sudoers file properly. The user (or group to which the
           user belongs) should have the following line:

           <user> ALL = NOPASSWD: /usr/sbin/hb_report

           See the sudoers(5) man page for more details.

       Times
           In order to find files and messages in the given period and to parse the -f and -t options, hb_report uses perl and one of the
           Date::Parse or Date::Manip perl modules. Note that you need only one of these. Furthermore, on nodes which have no logs and where
           you don't run hb_report directly, no date parsing is necessary. In other words, if you run this on a loghost then you don't need
           these perl modules on the cluster nodes.

           On rpm based distributions, you can find Date::Parse in perl-TimeDate and on Debian and its derivatives in libtimedate-perl.

       Core dumps
           To backtrace core dumps gdb is needed and the packages with the debugging info. The debug info packages may be installed at the
           time the report is created. Let's hope that you will need this really seldom.

#TIMES
       Specifying times can at times be a nuisance. That is why we have chosen to use one of the perl modules--they do allow certain freedom
       when talking dates. You can either read the instructions at the Date::Parse examples page. or just rely on common sense and try stuff
       like:

           3:00          (today at 3am)
           15:00         (today at 3pm)
           2007/9/1 2pm  (September 1st at 2pm)
           Tue Sep 15 20:46:27 CEST 2009 (September 15th etc)

       hb_report will (probably) complain if it can't figure out what do you mean.

       Try to delimit the event as close as possible in order to reduce the size of the report, but still leaving a minute or two around for
       good measure.

       -f is not optional. And don't forget to quote dates when they contain spaces.

