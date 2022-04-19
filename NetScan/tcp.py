from email import message
import socket
from scapy.packet import Raw
from scapy.sendrecv import sr1
from scapy.supersocket import StreamSocket
import os

class tcpStack():
    def TCProbe():
        s = socket.socket()
        hostname = input("请输入要探测的主机IP或地址\n")
        des_port = input("请输入要探测的端口号\n")
        s.connect((hostname,int(des_port)))
        ss = StreamSocket(s, Raw)
        def MessageSending(message):
            if message == "Y" or message == "y":
                sending_message = input("请输入想要发送的信息")
                ss.sr1(Raw("Host:" + hostname + \
                "接收状态: successfully sent" + \
                "所发送的信息是:" + sending_message ))
                os._exit()
            elif message == "N" or message == "n":
                print("结束探测")
                os._exit()
if __name__ == "__main__":
    tcpStack()
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
