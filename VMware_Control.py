#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
 date:3/6/2022
 author:Cla1r3
 Roll back the virtual machine to the specified snapshot,
 then take the snapshot after a specified time of running
"""
import os
import subprocess
import sys
import time
import shutil


#host_list: List of hostnames to be operated
#operation: Operations to be performed

vmrun = r'<Directory path> of vmrun.exe'

vmx_map = {'<The name of Virtual Machine>': "<The name of the Virtual Machine's vmx file>"}

operation_map = {'start': r' -T ws start ',
                 'stop': r' -T ws stop ',
                 'revSnap': r' -T ws revertToSnapshot ',
                 'createSnap': r' -T ws snapshot ',
                }

def revSnap(host, operation: str):
    if not vmx_map.__contains__(host):
        print(host + "Host does not exist!")
        sys.exit()
    if not operation_map.__contains__(operation):
        print(operation + "Operation is illegal!")
        sys.exit()

    SnapshotName = r' <Name of the snapshot to roll back>'
    revSnap = vmrun + operation_map[operation] + vmx_map[host]+ SnapshotName
    subprocess.Popen(revSnap)


def CreateSnap(host, operation: str, name):
    if not vmx_map.__contains__(host):
        print(host + "Host does not exist!")
        sys.exit()
    if not operation_map.__contains__(operation):
        print(operation + "Operation is illegal!")
        sys.exit()

    filename =  os.path.splitext(name)[0]
    SnapshotName = r' '+ filename
    print("SnapshotName is :",SnapshotName)
    revSnap = vmrun + operation_map[operation] + vmx_map[host]+ SnapshotName
    subprocess.Popen(revSnap)


def operate(host, operation: str):
    if not vmx_map.__contains__(host):
        print(host + "Host does not exist!")
        sys.exit()
    if not operation_map.__contains__(operation):
        print(operation + "Operation is illegal!")
        sys.exit()

    cmd = vmrun + operation_map[operation] + vmx_map[host]
    subprocess.Popen(cmd)


def copyandrename(dumpath1,name,count,onefamilycount):
    '''
    Copy the snapshot file of the virtual machine to the folder waiting
    to be processed and name it according to the malware family.
    1. Copy to the target folder
    2. Rename
    '''
    time.sleep(3)
    path = r"<Directory of the virtual machine>"
    tardir = dumpath1
    filename ='Win10x641607-Snapshot'+ str(count) +'.vmem'
    shutil.move(path + '/' + filename, tardir + '/' + filename)

    Olddir = os.path.join(tardir, filename)
    newfilename = os.path.splitext(name)[0]


    filetype = '.vmem'
    Newdir = os.path.join(tardir, newfilename + filetype)
    time.sleep(3)
    os.rename(Olddir, Newdir)
    return True

if __name__ == '__main__':
    hosts = "Win10x641607"
    count = 0

    #Folder directory where snapshots are saved
    dumpath =r"D:\MmoryLoad\cridex-dumps"

    with open(r"cridexpath", 'r+', encoding='u8') as fp:
        SampleNames = fp.readlines()
        onefamilycount = 0
        for name1 in SampleNames:
            name = name1.replace('\n', '')
            print(name)
            time.sleep(2)
            revSnap(hosts, 'revSnap')
            time.sleep(2)
            operate(hosts, 'start')
            time.sleep(120)
            CreateSnap(hosts, 'createSnap', name)
            time.sleep(2)

            count = count + 1
            copyandrename(dumpath,name,count,onefamilycount)
