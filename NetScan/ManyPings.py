#!/usr/bin/env python3
# -*- coding:UTF-8 -*-
from multiprocessing import freeze_support
from multiprocessing.pool import ThreadPool
from datetime import datetime
import subprocess
import ipaddress
import threading
import logging
import sys

# ip网段文本路径(当前目录下)
IP_INFO_PATH = 'ip_list.txt'
# 线程数()
THREADING_NUM = 10
# 进程池
pool = ThreadPool(THREADING_NUM)
# 线程锁
queueLock = threading.Lock()

# 打印消息
def show_info(msg):
    queueLock.acquire()
    print(msg)
    queueLock.release()

# 读取文本，获取ip网段信息
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

def do_one_ping(target_ip):
    """
    单机ping测试
    """
    res = ''
    if sys.platform == 'linux':
        res = subprocess.run(['ping', '-c', '2', '-W', '1000', target_ip], stdout=subprocess.PIPE)
        res_out = str(res.stdout.decode('gbk'))
    if sys.platform == 'win32':
        res = subprocess.call(['ping', '-n', '2', '-w', '1000', target_ip ], stdout = subprocess.PIPE)
    else:
        show_info('不支持该平台系统，非常抱歉!')
    # print(f'res状态是: {res}')
    if res.returncode == 0:
        show_info('%-20s%-20s' % (target_ip, 'success'))

    else:
        show_info('%-20s%-20s' % (target_ip, 'failure'))

def do_ping(target_ip):
    """
    批量ping测试
    """
    try:
        res , res_out  = '', ''
        # 判断系统平台，执行对应命令
        if sys.platform == 'linux':
            res = subprocess.run(['ping', '-c', '2', '-W', '1000', target_ip], stdout=subprocess.PIPE)
            res_out = str(res.stdout.decode('gbk'))
        # 判断系统平台，执行对应命令
        if sys.platform == 'win32':
            res = subprocess.run(['ping', '-n', '2', '-w', '1000', target_ip ], stdout = subprocess.PIPE)
            res_out = str(res.stdout.decode('gbk'))
        else:
            show_info('不支持该平台系统，非常抱歉!')

        # print(f'res状态是: {res.returncode}')
        if res.returncode == 0:
            show_info('%-20s%-20s' % (target_ip, 'success'))
            # ping成功
            with open('log' + '/' + 'success_ping_result_' + LogTime + '.txt', 'a+') as f:
                f.write('%-20s%-20s' % (target_ip, 'success') + '\n')
            # ping成功之后，拿去给下一步的traceroute
            with open('log' + '/' + 'success_ping_result_for_trace' + '.txt', 'a+') as f:
                f.write('%-20s%-20s' % (target_ip,'') + '\n')
            # 放一个在同文件夹下，拿去traceroute
            with open('success_ping_result_for_trace' + '.txt', 'a+') as f:
                f.write('%-20s%-20s' % (target_ip,'') + '\n')
            # ping成功结果记录
            with open('log' + '/' + 'record_ping_' + LogTime + '.txt', 'a+') as f:
                f.write(res_out)
                f.write('-' * 50)
        else:
            show_info('%-20s%-20s' % (target_ip, 'failure'))
            # ping失败
            with open('log' + '/' + 'failure_ping_result_' + LogTime + '.txt', 'a+') as f:
                f.write('%-20s%-20s' % (target_ip, 'failure') + '\n')
            # ping失败结果记录
            with open('log' + '/' + 'record_ping_' + LogTime + '.txt', 'a+') as f:
                f.write(res_out)
                f.write('-' * 50)

    except Exception as e:
        show_info(e)

def get_ip_list(ip):
    """
    获取ip列表
    """
    temp = ipaddress.ip_network(ip, False).hosts()
    ip_list = []
    for item in temp:
        ip_list.append(str(item))
    # print(ip_list)
    return ip_list

freeze_support()
LogTime = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
start_time = datetime.now()

# 单主机ping
# do_one_ping('host')

# 批量执行ping
ips_list = get_ips_info()
for ips in ips_list:
    ip_list = get_ip_list(ips)
    for ip in ip_list:
        pool.apply_async(do_ping, args=(ip,))
pool.close()
pool.join()
def out():
    end_time = datetime.now()
    print('All done.总花费时间{:0.2f}s.'.format((end_time - start_time).total_seconds()))