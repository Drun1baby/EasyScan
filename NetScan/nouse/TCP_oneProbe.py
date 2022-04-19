from email import message
import re
import socket
from scapy.packet import Raw
from scapy.sendrecv import sr1
from scapy.supersocket import StreamSocket
import os
import sys

class tcpStack():
    def TCProbe(hostname,des_port):
        s = socket.socket()
        s.connect((hostname,int(des_port)))
        ss = StreamSocket(s, Raw)
        message = input("主机存活!   Do you want to send a message? [Y/N]")
        if message == "Y" or message == "y":
            sending_message = input("请输入想要发送的信息")
            ss.sr1(Raw("Host:" + hostname + "    接收状态: successfully sent" + "    所发送的信息是:    " + sending_message ))
            sys.exit()
        elif message == "N" or message == "n":
            print("结束探测")
            sys.exit()
'''
    try:
        tcpStack.TCProbe()
        try:
            message = input("主机存活!   Do you want to send a message? [Y/N]")
            tcpStack.TCProbe.MessageSending(message)
        except:
            print("try again")
    except:
        print("输入的参数不合规，请重新输入")
        try:
            tcpStack.TCProbe()
            message = input("主机存活!   Do you want to send a message? [Y/N]")
        except:
            print("输入的参数不合规")
'''
if __name__ ==