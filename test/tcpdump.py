# -*- coding: utf-8 -*-

# !/bin/env python
import time
import datetime
import subprocess as sub
from optparse import OptionParser
import os, sys
import socket


def dump_dict(flow_dict, timestr, log_file, top_n, debug):
    try:
        timestamp = datetime.datetime.fromtimestamp(int(time.time())).strftime(timestr)
    except Exception as e:
        print(e)
        sys.exit(1)

    # get top values
    top_n_list = sorted(flow_dict.iteritems(), key=lambda x: -x[1])[:top_n]
    for item in top_n_list:
        line = 'time=%s`src_ip=%s`src_port=%s`dst_ip=%s`dst_port=%s`bytes=%s' % (
            timestamp, item[0][0], item[0][1], item[0][2], item[0][3], item[1])
        log_file.write(line + '\n')
        if debug: print(line)
    log_file.flush()


def get_host_ip():
    return socket.gethostbyname(socket.gethostname())


def add_bytes_to_dict(line_list, flow_dict):
    '''
    accept a list which contains tcpdump info, and set into the dictionary given as the second arg.
    the tcpdump info line is like this:
    ['IP', '10.46.64.148.9922', '>', '100.84.32.188.56300:', 'tcp', '100']
    '''

    src_ip = '.'.join(line_list[1].split('.')[0:4])
    src_port = line_list[1].split('.')[4]
    dst_ip = '.'.join(line_list[3].split('.')[0:4])
    dst_port = line_list[3].split('.')[4].strip(':')
    bytes = int(line_list[5])
    tmp_key = (src_ip, src_port, dst_ip, dst_port)
    if tmp_key in flow_dict.keys():
        flow_dict[tmp_key] += bytes
    else:
        flow_dict[tmp_key] = bytes


def x_parser():
    parser = OptionParser()
    parser.add_option("-i", "--interval", action="store", dest="INTERVAL",
                      help="dump result every INTERVAL seconds, default 60")
    parser.add_option("-f", "--file", action="store", dest="FILE", help="Where the data file should be, REQUIRED")
    parser.add_option("-D", "--debug", action="store_true", dest="isDebug", default=False,
                      help="open debug mode if selected(only print to stddin)")
    parser.add_option("-n", "--topn", action="store", dest="TOPN", help="top n values to dump, default 50")
    parser.add_option("-e", "--expression", action="store", dest="EXPRESSION",
                      help="this arg will pass to tcpdump, ext. 'tcp src port 80', REQUIRED")
    parser.add_option("-T", "--timeStr", action="store", dest="TIMESTR",
                      help="timeStamp format, default is like 'date +\"%Y-%m-%d %H:%M:%S\"'")
    return parser


def main():
    parser = x_parser()
    (options, args) = parser.parse_args()
    interval = int(options.INTERVAL or 60)
    timestr = options.TIMESTR or '''%Y-%m-%d %H:%M:%S'''
    top_n = int(options.TOPN or 50)
    # if not options.FILE:
    #     print("NO log file given, exit.")
    #     sys.exit(1)
    # else:
    #     log_file = open(options.FILE, 'w')
    log_file = open('2016-12-19.tcpdump', 'w')

    # dictionary use to keep the flow data,'(src_ip, src_port, dst_ip, dst_port)' as a key, value 'bytes'
    flow_dict_in = {}
    flow_dict_out = {}
    my_ip = get_host_ip()
    t1 = time.time()
    # if options.EXPRESSION:
    #     # please refer to tcpdump's man page for details, we don't need the packet's info when it's an ACK/SYN, so have this expression: (((ip[2:2]....!= 0)
    #     # and also shuld make tcpdump line buffer,that's why  we use '-l'
    #     p = sub.Popen(
    #         ['tcpdump', '(((ip[2:2] - ((ip[0]&0xf)<<2)) - ((tcp[12]&0xf0)>>2)) != 0) and tcp and ', options.EXPRESSION,
    #          '-l', '-nn', '-q', '-t'], stdout=sub.PIPE)
    # else:
    #     print("No expression given ,exit.")
    #     sys.exit(1)
    p = sub.Popen(
        ['tcpdump', '(((ip[2:2] - ((ip[0]&0xf)<<2)) - ((tcp[12]&0xf0)>>2)) != 0) and tcp and ', options.EXPRESSION,
         '-l', '-nn', '-q', '-t'], stdout=sub.PIPE)

    for line in iter(p.stdout.readline, b''):
        # the line contains '\n', hate it...
        line_list = line.strip().split(' ')
        if my_ip in line_list[1]:
            add_bytes_to_dict(line_list, flow_dict_out)
        elif my_ip in line_list[3]:
            add_bytes_to_dict(line_list, flow_dict_in)
        else:
            print("ERROR, don't know what it is: %s." % (line))
        t2 = time.time()

        # print the result every interval seconds, and zero out the dictionary,start again
        if t2 - t1 > interval:
            t1 = time.time()
            dump_dict(flow_dict_in, timestr, log_file, top_n, options.isDebug)
            dump_dict(flow_dict_out, timestr, log_file, top_n, options.isDebug)
            flow_dict_in = {}
            flow_dict_out = {}
    log_file.close()


if __name__ == '__main__':
    main()
