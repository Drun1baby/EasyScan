# -*- coding: UTF-8 -*-
import time 
import datetime, threading
from bs4 import BeautifulSoup
import subprocess
import sys

#fp2=open("exp.txt",'w')

def TraceRoute(hostname):
        number = 0
        #fp2.write(hostname)
        JudegHost =' '+ hostname + ' is the destination'
        #print(hostname)
        #subprocess.call(['traceroute',hostname])
        traceroute = subprocess.Popen(["tracert", '-w', '100', hostname],stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        while (True): # 先数据处理，再 Traceroute
                #nowTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                tmp1 = str(traceroute.stdout.readline())
                tmp2 = tmp1.replace("\\r\\n'",'')
                if len(tmp2) > 15:  # 数据处理
                    tmp3 = tmp2.replace("b'\\xcd\\xa8\\xb9\\xfd\\xd7\\xee\\xb6\\xe0 30 \\xb8\\xf6\\xd4\\xbe\\xb5\\xe3\\xb8\\xfa\\xd7\\xd9\\xb5\\xbd","")
                    tmp4 = tmp3.replace("\\xb5\\xc4\\xc2\\xb7\\xd3\\xc9","is the destination")
                    tmp5 = tmp4.replace("\\xc7\\xeb\\xc7\\xf3\\xb3\\xac\\xca\\xb1\\xa1\\xa3","Request Timeout")
                    hop = tmp5
                elif len(tmp2) > 0:
                    hop = tmp2
                if not hop: break
                print('-->',hop)
                with open('log' + '/' + 'TraceRoute_Mark'  + "  "+ hostname + '.txt', 'a+') as f:
                    f.write('%-20s%-20s' % (hop,'') + '\n')
                with open('TraceRoute_Mark'  + "  "+ hostname + '.txt', 'a+') as f:
                    f.write('%-20s%-20s' % (hop,'') + '\n')
                if JudegHost != hop:
                    if hostname in hop:
                        print("Traceroute is over")
                        print("<!-----不华丽的分割线---->")
                        print("<!-----不华丽的分割线---->\n")
                        break
                    elif "Request Timeout" in hop:
                        number = number + 1
                        if number > 20:
                            with open('log' + '/' + 'TraceRoute_Mark'  + "  "+ hostname + '.txt', 'a+') as f:
                                f.write('Traceroute Failed')
                            with open('TraceRoute_Mark'  + "  "+ hostname + '.txt', 'a+') as f:
                                f.write('Traceroute Failed')
                            print("到达最大跳数，追踪下一个 IP")
                            break


        #threading.Timer(60*50, TraceRoute).start()
# TraceRoute()
#LogTime = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
def main():
    try:
        with open('success_ping_result_for_trace.txt','r') as f:
            for line in f:
                line = line.rstrip()
                print('Now we are tracing   ' "{}".format(line))
                print("Relax Baby, have A Nice Day\n")
                TraceRoute(line)
    except FileNotFoundError as e:
        print("Can not find 'success_ping_result_for_trace.txt'")
    except IndexError as e:
        print("'success_ping_result_for_trace.txt' error ")

if __name__ =='__main__':
    main()
