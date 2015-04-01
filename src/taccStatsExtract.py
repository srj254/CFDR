#!/usr/bin/python

import sys
import re
import os
import pandas as pd
import numpy  as np
import scipy  as sp

attrDictionary = {
'vfs'		: ['Timestamp', 'Identifier', 'dentry_use', 'file_use', 'inode_use'],

'mdc'		: ['Timestamp', 'Identifier', 'ldlm_cancel,E', 'mds_close,E', 'mds_getattr,E', 'mds_getattr_lock,E', 'mds_getxattr,E', 'mds_readpage,E', 'mds_statfs,E', 'mds_sync,E', 'reqs,E', 'wait,E,U=us'],

'intel_pmc3'	: ['Timestamp', 'Identifier', 'PMC0,E,W=48', 'PMC1,E,W=48', 'PMC2,E,W=48', 'PMC3,E,W=48', 'PERFEVTSEL0,C', 'PERFEVTSEL1,C', 'PERFEVTSEL2,C', 'PERFEVTSEL3,C', 'FIXED_CTR0,E,W=48', 'FIXED_CTR1,E,W=48', 'FIXED_CTR2,E,W=48', 'FIXED_CTR_CTRL,C', 'PERF_GLOBAL_STATUS,C', 'PERF_GLOBAL_CTRL,C', 'PERF_GLOBAL_OVF_CTRL,C'],

'sysv_shm'	: ['Timestamp', 'Identifier', 'mem_used,U=B', 'segs_used'],

'intel_uncore'	: ['Timestamp', 'Identifier', 'PERF_GLOBAL_CTRL,C', 'PERF_GLOBAL_STATUS,C', 'PERF_GLOBAL_OVF_CTRL,C', 'FIXED_CTR0,E,W=48', 'FIXED_CTR_CTRL,C', 'ADDR_OPCODE_MATCH,C', 'PMC0,E,W=48', 'PMC1,E,W=48', 'PMC2,E,W=48', 'PMC3,E,W=48', 'PMC4,E,W=48', 'PMC5,E,W=48', 'PMC6,E,W=48', 'PMC7,E,W=48', 'PERFEVTSEL0,C', 'PERFEVTSEL1,C', 'PERFEVTSEL2,C', 'PERFEVTSEL3,C', 'PERFEVTSEL4,C', 'PERFEVTSEL5,C', 'PERFEVTSEL6,C', 'PERFEVTSEL7,C'],

'vm'		: ['Timestamp', 'Identifier', 'pgpgin,E,U=KB', 'pgpgout,E,U=KB', 'pswpin,E', 'pswpout,E', 'pgalloc_normal,E', 'pgfree,E', 'pgactivate,E', 'pgdeactivate,E', 'pgfault,E', 'pgmajfault,E', 'pgrefill_normal,E', 'pgsteal_normal,E', 'pgscan_kswapd_normal,E', 'pgscan_direct_normal,E', 'pginodesteal,E', 'slabs_scanned,E', 'kswapd_steal,E', 'kswapd_inodesteal,E', 'pageoutrun,E', 'allocstall,E', 'pgrotated,E'],

'net'		: ['Timestamp', 'Identifier', 'collisions,E', 'multicast,E', 'rx_bytes,E,U=B', 'rx_compressed,E', 'rx_crc_errors,E', 'rx_dropped,E', 'rx_errors,E', 'rx_fifo_errors,E', 'rx_frame_errors,E', 'rx_length_errors,E', 'rx_missed_errors,E', 'rx_over_errors,E', 'rx_packets,E', 'tx_aborted_errors,E', 'tx_bytes,E,U=B', 'tx_carrier_errors,E', 'tx_compressed,E', 'tx_dropped,E', 'tx_errors,E', 'tx_fifo_errors,E', 'tx_heartbeat_errors,E', 'tx_packets,E', 'tx_window_errors,E'],

'numa'		: ['Timestamp', 'Identifier', 'numa_hit,E', 'numa_miss,E', 'numa_foreign,E', 'interleave_hit,E', 'local_node,E', 'other_node,E'],

'llite'		: ['Timestamp', 'Identifier', 'read_bytes,E,U=B', 'write_bytes,E,U=B', 'direct_read,E,U=B', 'direct_write,E,U=B', 'dirty_pages_hits,E', 'dirty_pages_misses,E', 'ioctl,E', 'open,E', 'close,E', 'mmap,E', 'seek,E', 'fsync,E', 'setattr,E', 'truncate,E', 'flock,E', 'getattr,E', 'statfs,E', 'alloc_inode,E', 'setxattr,E', 'getxattr,E', 'listxattr,E', 'removexattr,E', 'inode_permission,E', 'readdir,E', 'create,E', 'lookup,E', 'link,E', 'unlink,E', 'symlink,E', 'mkdir,E', 'rmdir,E', 'mknod,E', 'rename,E'],

'block'		: ['Timestamp', 'Identifier', 'rd_ios,E', 'rd_merges,E', 'rd_sectors,E,U=512B', 'rd_ticks,E,U=ms', 'wr_ios,E', 'wr_merges,E', 'wr_sectors,E,U=512B', 'wr_ticks,E,U=ms', 'in_flight', 'io_ticks,E,U=ms', 'time_in_queue,E,U=ms'],

'cpu'		: ['Timestamp', 'Identifier', 'user,E,U=cs', 'nice,E,U=cs', 'system,E,U=cs', 'idle,E,U=cs', 'iowait,E,U=cs', 'irq,E,U=cs', 'softirq,E,U=cs'],

'osc'		: ['Timestamp', 'Identifier', 'read_bytes,E,U=B', 'write_bytes,E,U=B', 'ost_destroy,E', 'ost_punch,E', 'ost_read,E', 'ost_setattr,E', 'ost_statfs,E', 'ost_write,E', 'reqs,E', 'wait,E,U=us'],

'lnet'		: ['Timestamp', 'Identifier', 'tx_msgs,E', 'rx_msgs,E', 'rx_msgs_dropped,E', 'tx_bytes,E,U=B', 'rx_bytes,E,U=B', 'rx_bytes_dropped,E'],

'ib_ext'	: ['Timestamp', 'Identifier', 'port_select,C', 'counter_select,C', 'port_xmit_data,E,U=4B', 'port_rcv_data,E,U=4B', 'port_xmit_pkts,E', 'port_rcv_pkts,E', 'port_unicast_xmit_pkts,E', 'port_unicast_rcv_pkts,E', 'port_multicast_xmit_pkts,E', 'port_multicast_rcv_pkts,E'],

'tmpfs'		: ['Timestamp', 'Identifier', 'bytes_used,U=B', 'files_used']

}

requirement = ['vm'] # 'llite', 'block', 'osc', 'lnet']

def createNodeDictionary(nodePath):
	nodeDict = {}
	for dirpath, dirnames, filenames in os.walk(nodePath):
		for filename in filenames:
			filepath = os.path.join(dirpath, filename)
			if filename.split('.')[0] in attrDictionary.keys() and filename.split('.')[0] in requirement:
#				print filename.split('.')[0]
#				raw_input()
				pass
			else:
#				print filename, "Not in Keys()"
				continue

			try:
				df = pd.io.parsers.read_csv(filepath, sep='\t', names=attrDictionary.get(filename.split('.')[0]), header=None)
				df = pd.DataFrame.sort(df, columns='Timestamp')
#				print pd.DataFrame.to_string(df)
			except pd._parser.CParserError:
				df = None
			key = filename.split('.')[0]
			nodeDict[key] = df
	return nodeDict

def createTaccDB(nodesPath):
	nodesDict={}
	i = 0
	for dirpath, dirnames, filenames in os.walk(nodesPath):
		for dirname in dirnames:
			i +=1
			nodeNumber = int((dirname.split('.')[0].split('-')[1])[1:])
			nodesDict[nodeNumber] = createNodeDictionary(os.path.join(dirpath, dirname))
	return nodesDict

def extractTaccStats(taccDB, node, key, feature, start, end):
	nodeDict = taccDB.get(node)
#	nodeDict = taccDB.get(taccDB.keys()[0])
	df 	 = nodeDict.get(key)
	roi_df   = df[(df['Timestamp'] >= start) & (df['Timestamp'] <= end)]
	column   = roi_df[feature]
	return column.tolist()
	
if __name__ == "__main__":
	if len(sys.argv) != 7:
		print "Usage: ./<ScriptName> <TaccStatsFilePath> <NodeNumber> <keyAttr> <feature> <start_time> <end_time>"
		exit()
	taccDB 	  = createTaccDB(sys.argv[1])
	dfExtract = extractTaccStats(taccDB, int(sys.argv[2]), sys.argv[3], sys.argv[4], int(sys.argv[5]), int(sys.argv[6]))
#	mylist =  (dfExtract['rd_merges,E'])
#	print mylist.tolist()
