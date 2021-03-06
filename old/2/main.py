#! /usr/bin/env python

import sys, re, os
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
    self.onlineDict = {}
    self.pluginsDict = {} 
    
    #Initialize a QTimer to run background updates (online players, status, new chat messages, etc)
    self.repeatingTimer = QtCore.QTimer()
    self.singleTimer = QtCore.QTimer() #Not used...
    
    self.s=Server()
    QtGui.QWidget.__init__(self, parent)
    self.ui = Ui_MainWindow()
    self.ui.setupUi(self)
    self.initUI()
    
    self.startRepeatingTimer()
    self.findPlugins() #Find the currently installed plugins by searching the plugin folder
    
    #Set the start/stop button text
    if self.s.status():
      self.ui.pushButtonStopStart.setText('Stop Server')
    else:
      self.ui.pushButtonStopStart.setText('Start Server')
    
  def initUI(self):
    self.connect(self.ui.pushButtonStopStart, QtCore.SIGNAL('clicked()'), self.stopStartClicked)
    self.connect(self.ui.lineEditMessage, QtCore.SIGNAL('returnPressed()'), self.sendChat)
    self.connect(self.ui.lineEditConsole, QtCore.SIGNAL('returnPressed()'), self.sendConsole)
    self.connect(self.ui.treeWidgetPluginList, QtCore.SIGNAL('itemSelectionChanged()'), self.pluginNameClicked)
    
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
    message = str(self.ui.lineEditMessage.text())
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
    message = str(self.ui.lineEditConsole.text())
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
  
  def updatePlayersDisplay(self):
    self.ui.treeWidgetPlayersList.clear()
    for name in self.onlineDict:
      a = QtGui.QTreeWidgetItem(self.ui.treeWidgetPlayersList)
      a.setText(0, name)
      childrenList = []
      for key in self.onlineDict[name]:
        w = QtGui.QTreeWidgetItem(a)
        w.setText(0, str(key) + ': ' + str(self.onlineDict[name][key]))
        a.insertChild(0, w)
  
  def updatePluginsList(self):
    for pluginName in self.pluginsDict.keys():
      a = QtGui.QTreeWidgetItem(self.ui.treeWidgetPluginList)
      a.setText(0, str(pluginName))
      
  def pluginNameClicked(self):
    pluginName = str(self.ui.treeWidgetPluginList.currentItem().text(0))
    lines = ''
    for line in self.pluginsDict[pluginName]:
      lines = lines + line + '\n'
    self.ui.textBrowserPlugin.setText(lines)

      	
#####################
#Other methodsprint
#####################

  def findPlugins(self):
    bukkitDir = os.path.split(self.s.startupScript)[0]
    pluginsDir = os.path.join(bukkitDir, 'plugins')
    pluginsListRaw = os.listdir(pluginsDir)
    for plugin in pluginsListRaw: #Dont include it twice if there is a .jar and a folder with the same name
      pluginName = plugin.split('.')[0]
      if pluginName not in self.pluginsDict:
        self.pluginsDict[pluginName] = []
    self.updatePluginsList()
    

  def getNewServerLines(self):
    if self.lastServerLine == 'first run': #If we are first starting up the app, read back to the last reboot
      newServerLines = self.s.consoleReadTo(' [INFO] Stopping server')
    else:
      newServerLines = self.s.consoleReadTo(self.lastServerLine)
    if len(newServerLines) > 0:
      self.lastServerLine = newServerLines[-1]
    return newServerLines
    
  def routeServerLines(self):
  
    #Set up variables to monitor if we found any of the relevent lines. We do this so we dont have
    #to call their respective functions of nothing was found
    chatLinesWereFound = False
    playersChanged = False
    
    newServerLines = self.getNewServerLines()
    chatLines = []
    if len(newServerLines) > 0: #Don't waste your time if no new lines are found
      for line in newServerLines:
        matchChat = re.search(r'<\w+>', line)
        matchChat2 = re.search(r'\[CONSOLE\]', line)
        matchLoggedIn = re.search(r'(\d+\-\d+\-\d+ \d+:\d+:\d+) \[INFO\] (\w+) \[/(\d+\.\d+\.\d+\.\d+:\d+)\] logged in with entity id (\d+) at', line)
        matchLoggedOut = re.search(r'\] (\w+) lost connection: disconnect.quitting', line)
        matchLoggedOut2 = re.search(r'\] (\w+) lost connection: disconnect.endOfStream', line)
        matchPlugin = re.search(r'\d+\-\d+\-\d+ \d+:\d+:\d+ \[INFO\] \[(\w+)\]', line)
 
        if matchChat or matchChat2:
          chatLinesWereFound = True
          chatLines.append(line)
        
        if matchLoggedIn:
          playersChanged = True
          time = matchLoggedIn.group(1)
          name = matchLoggedIn.group(2)
          ip = matchLoggedIn.group(3)
          ID = matchLoggedIn.group(4)
          self.onlineDict[name] = {'Logged In':time[11:],
                                   'IP':ip,
                                   'ID':ID}
        
        if matchLoggedOut or matchLoggedOut2:
          playersChanged = True
          try:
            name = matchLoggedOut.group(1)
          except AttributeError:
            name = matchLoggedOut2.group(1)
          if name in self.onlineDict:
            del self.onlineDict[name]
            
        if matchPlugin:
          pluginName = matchPlugin.group(1)
          if pluginName in self.pluginsDict:
            self.pluginsDict[pluginName].append(line)
            
            
      self.updateConsoleDisplay(newServerLines)
      if chatLinesWereFound: self.updateChatDisplay(chatLines)
      if playersChanged: self.updatePlayersDisplay()
    return None
   
  def ticToc(self):
    self.updateStatusBar()
    self.routeServerLines()
  
  def startRepeatingTimer(self):
    self.repeatingTimer.start(1000)
  
  def updateStatusBar(self):
    if self.s.status():
      line = 'SERVER IS ON - Players Online: ' + str(len(self.onlineDict))
    else:
      line = 'SERVER IS OFF'
    self.ui.statusbar.showMessage(line)
      
    
    
if __name__ == "__main__":
  app = QtGui.QApplication(sys.argv)
  myapp = MyServer()
  myapp.show()
  sys.exit(app.exec_())
