#Descriptions
This directory include hb_report all the codes(implement with python). There are three classed, one environment variable configure and one lib. The following documents explain these files.

#Explainations
##master.py

The defination of master class, when user use the hb_report command, in the crm report script, some secure things is done, then crm script call master_node run function. Master do all things  master node should do, like decide to which log is collected, check ssh connections and so on.
##slave.py
The defination of slave class, this is a simple class, do collect log things and send the resule to master node.
##node.py
The defination of node class, it is the father class of master and slave class, abstract some common features about the subclass.
##envir.py
This is environment variable configure file, all the  variable is needed during the hb_report run.Kind of important
##utillib.py
This is functions library.
##corosync_conf_support.py
This is the corosync cluster support script, this script implement some unique function for corosync cluster
##ha_cf_support.py
This script just like corosync_conf_support.py, but this script for heartbeat cluster
##hb_report
This is hb_report entry script.
