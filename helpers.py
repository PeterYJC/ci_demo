#!/usr/bin/env python  
# -*- coding:utf-8 -*-
""" 
@author: peteryjc
@mail: yjcpeter@gmail.com
@file: helpers.py 
@time: 2019/12/01
"""

import socket


def communicate(host, port, request):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    s.send(request)
    response = s.recv(1024)
    s.close()
    return response
