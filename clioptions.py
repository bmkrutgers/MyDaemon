#!/usr/bin/env python3

import time
import  os
import sys
import array
import string


def creatSnapshot():
    print("Hi call the snapshot")
    return

def deleteSnapshot():
    print("Hi delete the snapshot")
    return

def addFile():
    print("Add/Modify Files")
    return

def renameFile(oldpFileName,newpFileName):
    print("rename File")
    print(oldpFileName)
    print(newpFileName)
    return

def deleteFile():
    print("deleteFile")
    return

def executeCloud9():
    file = open('fileResult.txt', 'r')
    content = file.read().splitlines()
    num_lines = sum(1 for line in open('fileResult.txt'))
    for fileVariable in range(0,num_lines):
        binaryArray = []
        arrayFile = content[fileVariable].split()
        oldpFileName = arrayFile[0]
        newpFileName = arrayFile[1]
        binaryArray.append(arrayFile[2])
        binaryArray.append(arrayFile[3])
        binaryArray.append(arrayFile[4])
        binaryArray.append(arrayFile[5])
        binarystr = ''.join(binaryArray)
        pFinalresult = int(binarystr, 2)
        if(pFinalresult == 1):
            renameFile(oldpFileName,newpFileName)
        elif(pFinalresult == 2):
            deleteFile()
        else:
            addFile()
    return

def options():
    while True:
        print("Hi")
        creatSnapshot()
        executeCloud9()
        deleteSnapshot()
        time.sleep(300)
        return