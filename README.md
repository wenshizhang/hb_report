#DESCRIPTION
The hb_report(1) is a utility to collect all information (logs, configuration files, system information, etc) relevant to Pacemaker (CRM) over the given period of time.
***
#OPTIONS
###dest
The report name. It can also contain a path where to put the report tarball. If left out, the tarball is created in the current directory named "hb_report-current_date", for instance hb_report-Wed-03-Mar-2010.

### -d
Don't create the compressed tar, but leave the result in a directory.
### -f { time | "cts:"testnum }
 The start time from which to collect logs. The time is in the format as used by the Date::Parse perl module. For cts tests, specify the "cts:" string followed by the test number. This option is required.

### -t time
 The end time to which to collect logs. Defaults to now.

### -n nodes
A list of space separated hostnames (cluster members). hb_report may try to find out the set of nodes by itself, but if it runs on the loghost which, as it is usually the case, does not belong to the cluster, that may be difficult. Also, OpenAIS doesn't contain a list of nodes and if Pacemaker is not running, there is no way to find it out automatically. This option is cumulative (i.e. use -n "a b" or -n a -n b).

### -l file
Log file location. If, for whatever reason, hb_report cannot find the log files, you can specify its absolute path.
### -E files
Extra log files to collect. This option is cumulative. By default, /var/log/messages are collected along with the cluster logs.

### -M

Don't collect extra log files, but only the file containing messages from the cluster subsystems.

### -L patt
 A list of regular expressions to match in log files for analysis. This option is additive (default: "CRIT: ERROR:").

### -p patt
Additional patterns to match parameter name which contain sensitive information. This option is additive (default: "passw.*").

### -Q      
Quick run. Gathering some system information can be expensive. With this option, such operations are skipped and thusinformation collecting sped up. The operations considered I/O or CPU intensive: verifying installed packages content, sanitizing files for sensitive information, and producing dot files from PE inputs.
### -A
This is an OpenAIS cluster. hb_report has some heuristics to find the cluster stack, but that is not always reliable. By default, hb_report assumes that it is run on a Heartbeat cluster.
### -u user
The ssh user. hb_report will try to login to other nodes without specifying a user, then as "root", and finally as "hacluster". If you have another user for administration over ssh, please use this option.

### -X ssh-options
Extra ssh options. These will be added to every ssh invocation. Alternatively, use $HOME/.ssh/config to setup desired ssh connection options.

### -S
Single node operation. Run hb_report only on this node and don't try to start slave collectors on other members of the cluster. Under normal circumstances this option is not needed. Use if ssh(1) does not work to other nodes.

### -Z

If the destination directory exist, remove it instead of exiting (this is default for CTS).

### -V
Print the version including the last repository changeset.

### -v
Increase verbosity. Normally used to debug unexpected behaviour.

### -h
Show usage and some examples.

### -D (obsolete)
Don't invoke editor to fill the description text file.

### -e prog (obsolete)
Your favourite text editor. Defaults to $EDITOR, vim, vi, emacs, or nano, whichever is found first.

### -C (obsolete)
Remove the destination directory once the report has been put in a tarball.

***

#EXAMPLES
Last night during the backup there were several warnings encountered (logserver is the log host):
```
           logserver# hb_report -f 3:00 -t 4:00 -n "node1 node2" report
```
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

