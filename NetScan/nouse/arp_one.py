import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
from scapy.all import *

def scapy_arp_one(ip_address, queue = None):
    packet = Ether(dst = 'FF:FF:FF:FF:FF:FF:FF:FF')/ARP(op = 1, hwdst = '00:00:00:00:00:00', pdst = ip_address)
    result_raw = srp(packet,timeout = 1,verbose=False)

    try:
        result_list = result_raw[0].res

        if queue == None:
            return result_list[0][1].getlayer(ARP.fields['hwsrc'])

    except:
        return

if __name__ == '__main__':
    list = scapy_arp_one("192.168.1.1")
    print(list)