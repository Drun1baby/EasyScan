# -*- coding:UTF-8 -*-
from scapy.all import *
from multiprocessing import freeze_support
from multiprocessing.pool import ThreadPool
from datetime import datetime
import subprocess
import ipaddress
import threading
import logging
import sys

IP_INFO_PATH = 'success_ping_result_for_trace.txt'

PACKET_TYPE = "echo-request"
TTL_EXCEED = 11
PACKET_VERBOSE = 0
THREADING_NUM = 10
queueLock = threading.Lock()

def show_info(msg):
    queueLock.acquire()
    print(msg)
    queueLock.release()


def get_ips_info():
    try:
        with open(IP_INFO_PATH, 'r') as f:
            for line in f.readlines():
                # 去掉前后空白
                line = line.strip()
                # 忽略空格行，len=1
                if (
                        len(line) == 1 or
                        line.startswith('#')
                ):
                    continue

                yield line

    except FileNotFoundError as e:
        show_info('Can not find "{}"'.format(IP_INFO_PATH))
    except IndexError as e:
        show_info('"{}" format error'.format(IP_INFO_PATH))
'''
从 packet 中获取 IP
'''
def get_ip_from_packet(packet):
    return packet[IP].src


def reach_host(response_packet):
    return response_packet[ICMP].type != TTL_EXCEED

'''
时间转换
'''

def seconds_to_ms(seconds):
    return format(seconds / 60 * 1000, '.2f')

'''
ICMP 发包
'''

def hop(address, ttl, timeout):
    my_packet = IP(dst=address, ttl=ttl) / ICMP(type=PACKET_TYPE)
    return sr1(my_packet, timeout=timeout, verbose=PACKET_VERBOSE)

'''
traceroute 状态
'''

def print_status_message(success, ttl, response_time=None, ip=None):
    if success:
        response_ms_time = seconds_to_ms(response_time)
        message = f"{ttl})  {response_ms_time} ms {ip}"
        with open('log' + '/' + 'success_ping_result_' + ip + '.txt', 'a+') as f:
                f.write('%-20s%-20s' % (ip, 'success') + '\n')
    else:
        message = f"{ttl})     * * *    Request Time Out."

    print(message)

'''
函数 trace 用来执行 traceroute 操作
'''

def trace(ip, max_hops, timeout, verbose, number):
    ttl = 1
    stations = []
    while ttl <= max_hops:
        start_time = time.time()
        response_packet = hop(ip, ttl, timeout)
        final_time = time.time() - start_time
        if response_packet:
            ip = get_ip_from_packet(response_packet)
            stations.append(ip)
            if verbose:
                print_status_message(True, ttl, final_time, ip)
            if reach_host(response_packet):
                break
        else:
            stations.append(None)
            if verbose:
                print_status_message(False, ttl)
        ttl += 1
    return stations

'''
使用 shell 的 tracert 指令

def do_one_traceroute(ip):
    res = ''
    if sys.platform == 'linux':
        res = subprocess.run(['traceroute', ip], stdout=subprocess.PIPE)
        res_out = str(res.stdout.decode('gbk'))
    if sys.platform == 'win32':
        res = subprocess.Popen(['tracert', ip], shell=True) 
    else:
        show_info('不支持该平台系统，非常抱歉!')
'''
def get_ips_from_file(filename):
    ips = []
    try:
        with open(filename, 'r') as f:
            for line in f.readlines():
                line = line.strip()
                ips.append(line.strip())
    except FileNotFoundError as e:
        show_info('Can not find "{}"'.format(filename))
    except IndexError as e:
        show_info('"{}" format error'.format(filename))
    
    return ips

def main():
    filename = 'success_ping_result_for_trace.txt'
    host = []
    host = get_ips_from_file(filename)
    for i in range(0,len(host)):
        ip = host[i]
        print("Now tracing IP {}".format(ip))
        print("<!-----不华丽的分割线---->")
        trace(ip, max_hops = 8, timeout = 5, verbose = True, number=int(i)+1)
if __name__ == '__main__':
    main()