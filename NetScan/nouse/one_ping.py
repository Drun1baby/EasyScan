import logging
logging.getLogger("scrapy.runtime").setLevel(logging.ERROR)
from scapy.all import *
from random import randint 
def scapy_ping_one(host):
    id_ip = randint(1,65535) #构建ip数据包随机Id 
    id_ping = randint(1,65535) #构建ICMP数据包随机ID
    seq_ping = randint(1,65535) #构建随机序列号，相当于我们的计算机进程ID
    packet = IP(dst=host,ttl=64,id=id_ip)/ICMP(id=id_ping,seq=seq_ping)/b'lich'
    ping=sr1(packet,timeout=2,verbose=False)
    ping.show()
    if ping:
        os. exit(3)
ip = input()
scapy_ping_one(ip) 