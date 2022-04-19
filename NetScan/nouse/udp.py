import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
from scapy.all import *

def scapy_udp_scan(hostname,lport,hport):
    result_raw = sr(IP(dst=hostname)/UDP(dport=int(lport))/'Hello world',
                    timeout=1,verbose=False)
    scan_port = []

    for x in range(lport,hport):
        scan_port.append(x)
    
    port_not_open = []
    result_list = scan_port
    for i in range(len(result_list)):
        print(result_list[i])
        if result_list[i][1].haslayer(ICMP):
            port_not_open.append(result_list[i][1][3].fields['dport'])
rlt = scapy_udp_scan('124.222.21.138',9000,9002)
print('开放端口如下: ')
print(rlt)