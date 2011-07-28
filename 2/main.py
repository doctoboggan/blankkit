#! /usr/bin/python

import sys, re
import utils
from Server import Server
from PyQt4 import QtCore, QtGui
from interface import Ui_MainWindow

class MyServer(QtGui.QMainWindow):
  
  def __init__(self, parent=None):
    #Instance variables
    self.chatLines = []
    self.consoleLines = []
    self.lastServerLine = 'first run'
    self.playerCount = 0  
    
    #Initialize a QTimer to run background updates (online players, status, new chat messages, etc)
    self.repeatingTimer = QtCore.QTimer()
    self.singleTimer = QtCore.QTimer()
    
    self.s=Server()
    QtGui.QWidget.__init__(self, parent)
    self.ui = Ui_MainWindow()
    self.ui.setupUi(self)
    self.initUI()
    
    self.startRepeatingTimer()  
    
    #Set the start/stop button text
    if self.s.status():
      self.ui.pushButtonStopStart.setText('Stop Server')
    else:
      self.ui.pushButtonStopStart.setText('Start Server')
    
  def initUI(self):
    self.connect(self.ui.pushButtonStopStart, QtCore.SIGNAL('clicked()'), self.stopStartClicked)
    self.connect(self.ui.lineEditMessage, QtCore.SIGNAL('returnPressed()'), self.sendChat)
    self.connect(self.ui.lineEditConsole, QtCore.SIGNAL('returnPressed()'), self.sendConsole)
    
    #Connect the timer
    self.connect(self.repeatingTimer, QtCore.SIGNAL('timeout()'), self.ticToc)


#####################
#GUI control methods
#####################

  #Start or stop the server
  def stopStartClicked(self):
    if self.s.status():
      self.s.stop()
      self.updateStatusBar()
      self.ui.pushButtonStopStart.setText('Start Server')
    else:
      self.s.start()
      self.updateStatusBar()
      self.ui.pushButtonStopStart.setText('Stop Server')  

  def sendChat(self):
    message = self.ui.lineEditMessage.text()
    self.ui.lineEditMessage.clear()   
    if message != '':
      self.s.message(message)
    self. updateChatDisplay([])
          
  def updateChatDisplay(self, chatLines): 
    for line in chatLines:
      fixedLine = line[5:19] + line[26:]
      width = self.ui.treeWidgetChat.columnWidth(0)
      fixedLine = utils.wordWrap(width-5, fixedLine)
      a = QtGui.QTreeWidgetItem(self.ui.treeWidgetChat)
      a.setText(0, fixedLine)
    if len(chatLines):
      self.ui.treeWidgetChat.scrollToItem(a)
      self.chatLines.extend(chatLines)

  def sendConsole(self):
    message = self.ui.lineEditConsole.text()
    self.ui.lineEditConsole.clear()   
    if message != '':
      self.s.command(message)
    self. updateConsoleDisplay([])
          
  def updateConsoleDisplay(self, consoleLines): 
    for line in consoleLines:
      fixedLine = line[5:19] + line[26:]
      width = self.ui.treeWidgetConsole.columnWidth(0)
      fixedLine = utils.wordWrap(width-5, fixedLine)
      a = QtGui.QTreeWidgetItem(self.ui.treeWidgetConsole)
      a.setText(0, fixedLine)
    if len(consoleLines):
      self.ui.treeWidgetConsole.scrollToItem(a)
      self.consoleLines.extend(consoleLines)
  
  def updatePlayersDisplay(self, onlineDict):
    pass
      	
      	
#####################
#Other methods
#####################

  def getNewServerLines(self):
    if self.lastServerLine == 'first run':
      newServerLines = self.s.console(60)
      self.lastServerLine = newServerLines[-1]
    else:
      newServerLines = self.s.consoleReadTo(self.lastServerLine)
      if len(newServerLines) > 0:
        self.lastServerLine = newServerLines[-1]
    return newServerLines
    
  def routeServerLines(self):
    newServerLines = self.getNewServerLines()
    chatLines = []
    onlineDict = {}
    if len(newServerLines) > 0:
      for line in newServerLines:
        matchChat = re.search(r'<\w+>', line)
        matchChat2 = re.search(r'\[CONSOLE\]', line)
        matchLoggedIn = re.search(r'(\d+\-\d+\-\d+ \d+:\d+:\d+) \[INFO\] (\w+) \[/(\d+\.\d+\.\d+\.\d+:\d+)\] logged in with entity id (\d+) at', line)
        matchLoggedOut = re.search(r'\] (\w+) lost connection: disconnect.quitting', line)
        matchLoggedOut2 = re.search(r'\] (\w+) lost connection: disconnect.endOfStream', line)
 
        if matchChat or matchChat2:
          chatLines.append(line)
        
        if matchLoggedIn:
          time = matchLoggedIn.group(1)
          name = matchLoggedIn.group(2)
          ip = matchLoggedIn.group(3)
          ID = matchLoggedIn.group(4)
          onlineDict[name] = {'timeIn':time,
                              'IP':ip,
                              'ID':ID}
        
        if matchLoggedOut or matchLoggedOut2:
          try:
            name = matchLoggedOut.group(1)
          except AttributeError:
            name = matchLoggedOut2.group(1)
          if name in onlineDict:
            del onlineDict[name]
            
      self.playerCount = len(onlineDict)
            
      self.updateConsoleDisplay(newServerLines)
      self.updateChatDisplay(chatLines)
      self.updatePlayersDisplay(onlineDict)
    return None
      

  def ticToc(self):
    self.updateStatusBar()
    self.routeServerLines()
  
  def startRepeatingTimer(self):
    self.repeatingTimer.start(1000)
  
  def updateStatusBar(self):
    if self.s.status():
      line = 'SERVER IS ON - Players Online: ' + str(self.playerCount)
    else:
      line = 'SERVER IS OFF'
    self.ui.statusbar.showMessage(line)
      
    
    
if __name__ == "__main__":
  app = QtGui.QApplication(sys.argv)
  myapp = MyServer()
  myapp.show()
  sys.exit(app.exec_())