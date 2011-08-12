#! /usr/bin/python

import sys
import utils
from Server import Server
from PyQt4 import QtCore, QtGui
from interface import Ui_MainWindow

class MyServer(QtGui.QMainWindow):
  
  def __init__(self, parent=None):
  
    #Instance variables
    self.chatLines = []
    self.consoleLines = []
    self.lastServerLine = ''
    
    #Initialize a QTimer to run background updates (online players, status, new chat messages, etc)
    self.repeatingTimer = QtCore.QTimer()
    self.singleTimer = QtCore.QTimer()
    
    self.s=Server()
    QtGui.QWidget.__init__(self, parent)
    self.ui = Ui_MainWindow()
    self.ui.setupUi(self)
    self.initUI()
    
    self.startRepeatingTimer()
    self.sendMessageClicked()
    self.consoleClicked()
    self.onlineClicked()
    

    
    
  def initUI(self):
    self.connect(self.ui.pushButtonStart, QtCore.SIGNAL('clicked()'), self.startClicked)
    self.connect(self.ui.pushButtonStop, QtCore.SIGNAL('clicked()'), self.stopClicked)
    self.connect(self.ui.pushButtonStopStart, QtCore.SIGNAL('clicked()'), self.stopStartClicked)
    
    
    self.connect(self.ui.pushButtonStatus, QtCore.SIGNAL('clicked()'), self.statusClicked)
    self.connect(self.ui.pushButtonOnline, QtCore.SIGNAL('clicked()'), self.onlineClicked)
    
    self.connect(self.ui.pushButtonSendMessage, QtCore.SIGNAL('clicked()'), self.sendMessageClicked)
    self.connect(self.ui.lineEditMessage, QtCore.SIGNAL('returnPressed()'), self.sendMessageClicked)
    
    self.connect(self.ui.pushButtonConsole, QtCore.SIGNAL('clicked()'), self.consoleClicked)
    self.connect(self.ui.lineEditConsole, QtCore.SIGNAL('returnPressed()'), self.consoleClicked)
    
    #Connect the timer button
    self.connect(self.ui.pushButtonStartTimer, QtCore.SIGNAL('clicked()'), self.startRepeatingTimer)
    #Connect the timer
    self.connect(self.repeatingTimer, QtCore.SIGNAL('timeout()'), self.ticToc)
    
  def startClicked(self):
    self.s.start()
    self.checkStatus()
    
  def stopClicked(self):
    self.s.stop()
    self.checkStatus()
    
  def statusClicked(self):
    self.checkStatus()
    
  def onlineClicked(self):
    self.players = self.s.players()
    playersFormatted = ''
    if self.players == ['']:
      playersFormatted = 'No one online. Click to refresh'
    elif len(self.players) is 1 and self.players[0] != '':
      playersFormatted = self.players[0]
    else:
      for player in self.players:
        playersFormatted = playersFormatted + ' ' + player
    self.ui.labelOnline.setText(playersFormatted)
    
  def sendMessageClicked(self):

    message = self.ui.lineEditMessage.text()
    self.ui.lineEditMessage.clear()   
    if message != '':
      self.s.message(message)

    if len(self.chatLines) is 0:
      self.chatLines = self.s.chat(60)
      newChatLines = self.chatLines
    else:
      newChatLine = 'poop'
      searchBack = 0
      while newChatLine not in self.chatLines[-2:]:
        searchBack = searchBack + 1
        newChatLine = self.s.chat(searchBack, oneLine=True)
      newChatLines = self.s.chat(searchBack)
      newChatLines.pop(0)
      
    if len(newChatLines) > 0:
      for line in newChatLines:
        fixedLine = line[5:19] + line[26:]
        width = self.ui.treeWidgetChat.columnWidth(0)
        fixedLine = utils.wordWrap(width-5, fixedLine)
        a = QtGui.QTreeWidgetItem(self.ui.treeWidgetChat)
        a.setText(0, fixedLine)
      self.ui.treeWidgetChat.scrollToItem(a)
    self.chatLines.extend(newChatLines)

      
  def consoleClicked(self):

    message = self.ui.lineEditConsole.text()
    self.ui.lineEditConsole.clear()   
    if message != '':
      self.s.command(message)

    if len(self.consoleLines) is 0:
      self.consoleLines = self.s.console(60)
      newConsoleLines = self.consoleLines
    else:
      newConsoleLine = 'poop'
      searchBack = 0
      while newConsoleLine[0] not in self.consoleLines[-2:]:
        searchBack = searchBack + 1
        newConsoleLine = self.s.console(searchBack, 1)
      newConsoleLines = self.s.console(searchBack)
      newConsoleLines.pop(0)
      
    if len(newConsoleLines) > 0:
      for line in newConsoleLines:
        fixedLine = line[5:19] + line[26:]
        width = self.ui.treeWidgetConsole.columnWidth(0)
        fixedLine = utils.wordWrap(width-5, fixedLine)
        a = QtGui.QTreeWidgetItem(self.ui.treeWidgetConsole)
        a.setText(0, fixedLine)
      self.ui.treeWidgetConsole.scrollToItem(a)
    self.consoleLines.extend(newConsoleLines)
      	
  def stopStartClicked(self):
    if self.s.status():
      self.s.stop()
      self.checkStatus()
      self.ui.pushButtonStopStart.setText('Start Server')
    else:
      self.s.start()    	
      self.checkStatus()
      self.ui.pushButtonStopStart.setText('Stop Server')
      
  def backgroundCheck(self):
    if lastServerLine == '':
      newServerLines = self.s.console(50)
      	
      	
#####################
#Other methods
#####################

  def ticToc(self):
    self.checkStatus()
    self.consoleClicked()
    self.sendMessageClicked()
  
  def startRepeatingTimer(self):
    self.repeatingTimer.start(1000)
  
  def checkStatus(self):
    if self.s.status():
      self.ui.statusbar.showMessage('Server is on')
    else:
      self.ui.statusbar.showMessage('Server is off')
      
    
    
if __name__ == "__main__":
  app = QtGui.QApplication(sys.argv)
  myapp = MyServer()
  myapp.show()
  sys.exit(app.exec_())
