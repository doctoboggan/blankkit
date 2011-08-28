def remoteConn(HOST='jj.ax.lt', PORT=25562):
  import socket, QtCore

  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  s.connect((HOST, PORT))
  newLines = ''
  while 1:
    newData = s.recv(1024)
    if newData:
      newLines += newData
    else:
      if newLines:
        
  s.close()
