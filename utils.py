#! /usr/bin/env python

import paramiko

def openRemote(user, host, ffile, pswd):
  sshClient = paramiko.SSHClient()
  sshClient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
  sshClient.connect(host, username=user, password=pswd)
  sftpClient = sshClient.open_sftp()
  remoteFile = sftpClient.open(ffile)
  print remoteFile.readline()
  return remoteFile

def collapse(llist):
  collapsedList = []
  for item in llist:
    if item not in collapsedList:
      collapsedList.append(item)
  return collapsedList
  
def wordWrap(length, line):
  if len(line) < length:
    return line
  else:
    head = line[:length] + '\n'
    tail = line[length:]
    if len(tail) > length:
      q = wordWrap(length, tail)
      return head + q
  return head + tail

