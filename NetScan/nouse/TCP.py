import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
from scapy.all import *
from one_ping import scapy_ping_one

def scapy_tcp_scan(hostname, lport, hport):
    result_raw = sr(IP(dst = hostname)/TCP(dport = (int(lport),int(hport)),flags = 2), timeout = 1,verbose=False)

    results_list = result_raw[0].res

    for i in range(len(results_list)):
        if results_list[i][1].haslayer(TCP):
            tcp_fields = results_list[i][1].getlayer(TCP).fields
            if tcp_fields['flags'] == 18:
                print("端口号： '+str(tcp_fields['sport']) + 'is open")

if __name__ == '__main__':
    rlt = scapy_tcp_scan('192.168.3.131',20,65535)