# -*- coding:utf-8 -*-
from __future__ import print_function
from colorama import Fore, init
import argparse
import nmap3
import json

nmap = nmap3.Nmap()
nmapscan = nmap3.NmapScanTechniques()
def top_port_scan(target) :
    results_top_port_scan = nmap.scan_top_ports(target)
    print(Fore.CYAN + json.dumps(results_top_port_scan , indent=4 , sort_keys=True))

def os_detection(target) :
    results_os_detection = nmap.nmap_os_detection(target);
    print(Fore.CYAN + json.dumps(results_os_detection , indent=4 , sort_keys=True)) #MUST BE ROOT

def ver_detection(target):
    results_version_detection = nmap.nmap_version_detection(target)
    print(Fore.CYAN + json.dumps(results_version_detection , indent=4 , sort_keys=True)) #MUST BE ROOT

def tcp_scan(target):
    results_tcp_scan = nmapscan.nmap_tcp_scan(target)
    print(Fore.CYAN + json.dumps(results_tcp_scan , indent=4 , sort_keys=True))

def udp_scan(target):
    results_udp_scan = nmapscan.nmap_udp_scan(target)
    print(Fore.CYAN + json.dumps(results_udp_scan , indent=4 , sort_keys=True))

def ping_scan(target):
    results_ping_scan = nmapscan.nmap_ping_scan(target)
    print(Fore.CYAN + json.dumps(results_ping_scan , indent=4, sort_keys=True))


def main():
    print("在 ip_list.txt 文件下输入要探测的网段, 先进行存活探测")
    print(Fore.MAGENTA + """
 _____ _   _  ______ _   _      _   _____                 
/  __ \ | | ||___  /| \ | |    | | /  ___|                
| /  \/ | | |   / / |  \| | ___| |_\ `--.  ___ __ _ _ __  
| |   | | | |  / /  | . ` |/ _ \ __|`--. \/ __/ _` | '_ \ 
| \__/\ |_| |./ /___| |\  |  __/ |_/\__/ / (_| (_| | | | |
 \____/\___/ \_____/\_| \_/\___|\__\____/ \___\__,_|_| |_|
""")
    print("若要使用多点 Ping 功能, 则事先在'ip_list.txt'文件中输入 ")
    target = input(Fore.GREEN + "[+] Enter the target you want to scan : ")

    ch = int(input(Fore.YELLOW + """
        CHOOSE FROM THE FOLLOWING SCAN OPTIONS
        [1] COMMON PORT SCAN
        [2] TCP SCAN ( -sT )   
        [3] UDP SCAN ( -Su )
        [4] OS DETECTION ( -O ) {requires root privileges}
        [5] VERSION DETECTION ( -Sv ) {requires root privileges} 
        [6] Ping ( -P ) """))

    if ch==1:
        top_port_scan(target)
    elif ch==2:
        tcp_scan(target)
    elif ch==3:
        udp_scan(target)
    elif ch==4:
        os_detection(target)
    elif ch==5:
        ver_detection(target)
    elif ch==6:
        ping_scan(target)
    else:
        print(Fore.RED + "INVALID OPTION")

if __name__ == '__main__':
    main()
  