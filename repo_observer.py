#!/usr/bin/env python  
# -*- coding:utf-8 -*-
"""
@author: PeterYJC
@mail: yjcpeter@gmail.com
@file: repo_observer.py 
@time: 2019/12/03
"""

import argparse
import os
import re
import socket
import socketserver
import subprocess
import sys
import time

import helpers


def poll():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dispatcher-server",
                        help="dispatcher host:port, " \
                             "by default it uses localhost:8888",
                        default="localhost:8888",
                        action="store")
    parser.add_argument("repo", metavar="REPO", type=str,
                        help="path to the repository this will observer")
    args = parser.parse_args()
    dispatcher_host, dispatcher_port = args.dispatcher_server.split(":")
    while True:
        try:
            subprocess.check_output(["./update_repo.sh", args.repo])
        except subprocess.CalledProcessError as e:
            raise Exception("Could not update and check repository. " +
                            "Reason: %s" % e.output)

        if os.path.isfile(".commit_hash"):
            try:
                response = helpers.communicate(dispatcher_host,
                                               int(dispatcher_port),
                                               "status")
            except socket.error as e:
                raise Exception("Could not conmunicate with dispatcher server: %s" % e)
            if response == "OK":
                commit = ""
                with open(".commit_id", "r") as f:
                    commit = f.readline()
                response = helpers.communicate(dispatcher_host,
                                               int(dispatcher_port),
                                               "dispatch:%s" % commit)
                if response != "OK":
                    raise Exception("Could not dispatch the test: %s" %
                                    response)
                print
                "dispatched!"
            else:
                raise Exception("Could not dispatch the test: %s" % response)
    time.sleep(5)
