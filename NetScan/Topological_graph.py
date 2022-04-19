from graphviz import Digraph
from graphviz import Graph
import re
'''
绘制拓扑图
'''
def gra(ip,a):
    ni = Graph('G', filename="Log_Pic/traceroute {}".format(ip),format='png')
    ni.attr('node', shape='rarrow')
    for i in range (0,len(a)):
        if i != len(a):
            ni.node(str(i+1), a[i])
        else:
            ni.node(str(i+1), a[i])
    ni.attr('node', shape='star')
    ni.attr(rankdir='LR')

    ni.edges(['12', '23'])
    print(ni.source) 
    ni.view()

'''
读取路由 Trace
'''
def TraceFind(ip):
    try:
        number = 0
        a = []
        with open('TraceRoute_Mark  '+"{}".format(ip)+'.txt', 'r+') as f2:
        # with open('/log/TraceRoute_Mark'  + "  "+ ip + '.txt', 'r+') as f2:
            for everyIP in f2:
                tmp1 = everyIP.strip()
                if "Request Timeout" not in tmp1:
                    if "is the destination" not in tmp1:
                        if len(tmp1) >= 40:
                            tmp = []
                            tmp = tmp1.split('ms')
                            a.append(tmp[3])
                            if ip in tmp1:
                                break
                else:
                    continue
            gra(ip,a)
    except FileNotFoundError as e:
        print("Can not find 'success_ping_result_for_trace.txt'")
    except IndexError as e:
        print("'success_ping_result_for_trace.txt' error ")

'''
获取 ip
'''
def get_ips():
    try:
        with open('success_ping_result_for_trace.txt','r') as f:
            for line in f:
                line = line.strip()
                TraceFind(str(line))
    except FileNotFoundError as e:
        print("Can not find 'success_ping_result_for_trace.txt'")
    except IndexError as e:
        print("'success_ping_result_for_trace.txt' error ")

if __name__ == '__main__':
   # gra(ip = '10.1.32.21')
    get_ips()
