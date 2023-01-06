[![Security Status](https://www.murphysec.com/platform3/v3/badge/1609773218044137472.svg)](https://www.murphysec.com/accept?code=9f8c8de6878f5c6aa78424727031adbc&type=1&from=2&t=2)

# EasyScan
## 写在前面

made by Drun1baby，silly baby



## 功能实现 

run.py 实现单 IP 多功能

ManyPings.py;Success_Traceroute.py;Topological_graph.py 实现多 IP 单功能



### 1. 单 IP 多功能

一开始是使用 Scapy 的，但是后面发现 Scapy 的探测不够准确，于是使用了 subprocess



### 2. 多 IP 单功能

ping 网段探测存活

