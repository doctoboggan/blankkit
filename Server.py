#! /usr/bin/env python

import pexpect, pxssh, os, re, time, utils, paramiko

class Server:
  """
  Spawn a server object with myServer = Server()
  and enter one of the following commands:
  
  myServer.start()           -- Starts the minecraft server
  myServer.stop()            -- Stops a currently running minecraft server
  myServer.status()          -- returns the status of the minecraft server
  myServer.command('string') -- Sends a command to the server and returns the next line
  myServer.message('string') -- Sends string as a server message
  myServer.players()         -- List of active players
  myServer.console(n)        -- display the last n lines of the console
  myServer.chat(n)           -- print the last n lines of chat history
  
  If there is already a server running, the instantiated server will resume it,
  if not, you can start one with myServer.start().
  
  The server is run in a screen with title "mc" so you can resume it from
  any terminal with the command: "screen -rd mc"
  """


  #Initialize the object
  def __init__(self, user='sa', host='jj.ax.lt', pswd='1q2wedrf', remote=False):
    #Instance variables
    self.startupScript = '/Users/jack/.mcserver/start.sh'
    #self.startupScript = '/home/sa/bukkit/minecraft.sh'
    self.bukkitDir = os.path.split(self.startupScript)[0]

    self.remote=remote
    self.user=user
    self.host=host
    self.pswd=pswd

    if remote:
      self.remoteStatusPX = pxssh.pxssh()
      self.remoteStatusPX.login(host, user, pswd)
    
    #Check the server status. If it is already running, resume it
    if self.status():
      print 'Resuming already running server.'
      if self.remote:
        self.mcServer = pxssh.pxssh()
        self.mcServer.login(self.host, self.user, self.pswd)
        self.mcServer.sendline('screen -rd mc')
      else:
        self.mcServer = pexpect.spawn('screen -rd mc')
    else:
      print 'Server not running. Start with myServer.start()'

    
  #Start the server
  def start(self):
    print 'Starting server... ',
    if not self.status():
      if self.remote:
        self.mcServer = pxssh.pxssh()
        self.mcServer.login(self.host, self.user, self.pswd)
        self.mcServer.sendline('screen -S mc ' + self.startupScript)
      else:
        self.mcServer = pexpect.spawn('screen -S mc ' + self.startupScript, timeout=120)
      self.mcServer.expect('\[INFO\] Done')
      self.startupLines = self.mcServer.before.split('\n')
      print 'Started'
    else:
      print 'Server is already running'
  
  #Stop the server  
  def stop(self):
    print 'Stopping server... ',
    if self.status():
      self.mcServer.sendline('stop')
      self.mcServer.expect('\[screen is terminating\]')
      self.mcServer.kill
      print 'Stopped'
    else:
      print 'There is no server to stop.'
  
  #return the status of the server (True if server is on)
  def status(self):
    if self.remote:
      self.remoteStatusPX.sendline('screen -ls')
      self.remoteStatusPX.prompt()
      response = self.remoteStatusPX.before
    else:  
      screen = pexpect.spawn('screen -ls')
      screen.expect('Socket')
      response = screen.before
    match = re.search(r'\t\d+\.mc\t', response)
    if match:
      return True
    else:
      return False
      
  #Send a command to the server and (probably) return the next line
  def command(self, command, sleep=0.08):
    if self.status():
      self.mcServer.sendline(command)
      time.sleep(sleep)
      return self.console(1)[0]
    else:
      print 'There is no server running, start with myServer.start()'
    
  #Send message to players with /say command
  def message(self, messageString):
    if self.status():
      self.mcServer.sendline('say ' + messageString)
    else:
      print 'There is no server running, start with myServer.start()'
    
  #Return a list of active players
  def players(self, sleep = .07):
    if self.status():
      listResponse = self.command('list', sleep=sleep)
      if listResponse[27:45] == 'Connected players:':
        return listResponse[46:].replace(' ','').split(',')
      else:
        sleep = sleep + .07
        out =self.players(sleep=sleep)
        return out
    else:
      print 'There is no server running, start with myServer.start()'
    
  #Return a list the last n lines of the console stream. If numOfLines is specified,
  #only return that many lines starting from n lines back
  def console(self, n=10, numOfLines=0):
    bukkitDir = os.path.split(self.startupScript)[0]
    serverLogPath = os.path.join(bukkitDir, 'server.log')
    if self.remote:
      sshClient = paramiko.SSHClient()
      sshClient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
      sshClient.connect(self.host, username=self.user, password=self.pswd)
      sftpClient = sshClient.open_sftp()
      logFile = sftpClient.open(serverLogPath)
    else:
      logFile = open(serverLogPath, 'r')
    
    bytesBack=0
    newLinePos = []
    #This loop reads in reverse from the end of the file looking for newline characters
    #When it finds n+1 charaters it knows it has gone back far enough for n lines
    while len(newLinePos) < n+1:
      bytesBack += 1
      try: #If the file is shorter than the number of lines we requested, this will throw an IOError
        logFile.seek(0-bytesBack, os.SEEK_END)
      except IOError:
        bytesBack -= 1
        break
      print logFile.read(1)
      if logFile.read(1) == '\n':
        newLinePos.append(bytesBack) #Store the position of each newline character
    logFile.seek(0-bytesBack, os.SEEK_END)
    if numOfLines is not 0: #Keep the 0 case as all of the lines
      numOfLines = numOfLines + 1
    logFileDump = logFile.read(bytesBack-newLinePos[0-numOfLines])
    logFileLines = logFileDump.split('\n')
    logFile.close()
    logFileLines.pop(0)  
    return logFileLines
    
  #Return the last n lines of chat history, if oneLine is set true, only return the nth line back
  def chat(self, n=10, oneLine = False):
    searchBack = 500
    chatLines = []
    while len(chatLines) < n+1:
      logLines = self.console(searchBack,500)
      for line in logLines:
        match = re.search(r'<\w+>', line)
        match2 = re.search(r'\[CONSOLE\]', line)
        if match or match2:
          chatLines.append(line)
      searchBack = searchBack + 500
    if oneLine is False:
      return sorted(chatLines)[-n:]
    else:
      return sorted(chatLines)[-n]
     
  #This method is very similar to the console method above, except it searches back until it reaches
  #a specific line specified by readToLine
  def consoleReadTo(self, readToLine):
    serverLogPath = os.path.join(self.bukkitDir, 'server.log')
    if self.remote:
      sshClient = paramiko.SSHClient()
      sshClient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
      sshClient.connect(self.host, username=self.user, password=self.pswd)
      sftpClient = sshClient.open_sftp()
      logFile = sftpClient.open('/home/sa/bukkit/server.log')
    else:
      logFile = open(serverLogPath, 'r')
         
    bytesBack=0
    newLinePos = []
    currentLine = ''
    #This loop reads in reverse from the end of the file looking for the specified line
    while readToLine not in currentLine:
      bytesBack = bytesBack + 1
      logFile.seek(0-bytesBack, os.SEEK_END)
      if logFile.read(1) == '\n':
        newLinePos.append(bytesBack) #Store the position of each newline character
        if len(newLinePos)>1:
          currentLine = logFile.read((newLinePos[-1]-newLinePos[-2])-1)
          print currentLine
    logFileDump = logFile.read(newLinePos[-2])
    logFileLines = logFileDump.split('\n')
    logFile.close()
    return filter(None, logFileLines[0:-1]) 

def main():
  print Server.__doc__

if __name__ == '__main__':
  main()
