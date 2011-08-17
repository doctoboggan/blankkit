#! /usr/bin/env python

import sys, re, os
import utils
from Server import Server
from PyQt4 import QtCore, QtGui
from interface import Ui_MainWindow


#This class starts a thread and runs the function passed into it
class GenericThread(QtCore.QThread):
  def __init__(self, function, *args, **kwargs):
    QtCore.QThread.__init__(self)
    self.function = function
    self.args = args
    self.kwargs = kwargs

  def __del__(self):
    self.wait()

  def run(self):
    if self.args and self.kwargs:
      self.function(*self.args,**self.kwargs)
    elif self.args and not self.kwargs:
      self.function(*self.args)
    elif not self.args and self.kwargs:
      self.function(**self.kwargs)
    else:
      self.function()
    return


class MyServer(QtGui.QMainWindow):
  
  def __init__(self, parent=None):
    
    #Instantiate a minecraft server object
    self.s=Server(remote=True)

    #The usual
    QtGui.QWidget.__init__(self, parent)
    self.ui = Ui_MainWindow()
    self.ui.setupUi(self)
    self.initUI()

    #Instance variables
    self.chatLines = []
    self.consoleLines = []
    self.onlineDict = {}
    self.pluginsDict = {} 

    #Initialize a QTimer to run and connect it to ticToc
    self.repeatingTimer = QtCore.QTimer()
    self.repeatingTimer.start(1000)      
    self.connect(self.repeatingTimer, QtCore.SIGNAL('timeout()'), self.ticToc)

    #Instantiate a qThreadWatcher() to monitor server.log for changes and connect its signal
    #to newLineDetected
    self.fileWatcher = QtCore.QFileSystemWatcher(self)
    self.fileWatcher.addPath(os.path.join(self.s.bukkitDir, 'server.log'))
    self.connect(self.fileWatcher, QtCore.SIGNAL('fileChanged(QString)'), self.newLineDetected)

    #Find the currently installed plugins by searching the plugin folder
    self.findPlugins()
    
    #Set the start/stop button text
    if self.s.status():
      self.ui.pushButtonStopStart.setText('Stop Server')
    else:
      self.ui.pushButtonStopStart.setText('Start Server')

    #On app boot, read til the last time the server was started
    self.lastServerLine = ' [INFO] Stopping server'
    self.newLineDetected()


  def initUI(self):
    #Connect the UI buttons
    self.connect(self.ui.pushButtonStopStart, QtCore.SIGNAL('clicked()'), self.stopStartClicked)
    self.connect(self.ui.lineEditMessage, QtCore.SIGNAL('returnPressed()'), self.sendChat)
    self.connect(self.ui.lineEditConsole, QtCore.SIGNAL('returnPressed()'), self.sendConsole)
    self.connect(self.ui.treeWidgetPluginList, QtCore.SIGNAL('itemSelectionChanged()'), self.pluginNameClicked)

#####################
#GUI control methods
#####################

  #Start or stop the server
  def handleStopStart(self):
    if self.s.status():
      self.s.stop()
      setName = 'Start'
    else:
      self.s.start()
      setName = 'Stop'
    self.emit(QtCore.SIGNAL('stopStartDone(QString)'), setName)

  def stopStartDone(self, setName):
    self.ui.pushButtonStopStart.setEnabled(True)
    self.ui.pushButtonStopStart.setText(setName + ' Server')
    self.updateStatusBar()
    

  def stopStartClicked(self):
    self.ui.pushButtonStopStart.setEnabled(False)
    self.ui.statusbar.showMessage('Trying...')
    stopStartThread = GenericThread(self.handleStopStart)
    self.disconnect( self, QtCore.SIGNAL("stopStartDone(QString)"), self.stopStartDone )
    self.connect( self, QtCore.SIGNAL("stopStartDone(QString)"), self.stopStartDone )
    stopStartThread.start()

  def updateStatusBar(self):
    if self.s.status():
      line = 'SERVER IS ON - Players Online: ' + str(len(self.onlineDict))
    else:
      line = 'SERVER IS OFF'
    self.ui.statusbar.showMessage(line)

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
#Other methods
#####################

  #This function finds all the plugins in the plugins folder and stores them in a dict
  def findPlugins(self):
    bukkitDir = os.path.split(self.s.startupScript)[0]
    pluginsDir = os.path.join(bukkitDir, 'plugins')
    pluginsListRaw = os.listdir(pluginsDir)
    for plugin in pluginsListRaw: #Dont include it twice if there is a .jar and a folder with the same name
      pluginName = plugin.split('.')[0]
      if pluginName not in self.pluginsDict:
        self.pluginsDict[pluginName] = []
    self.updatePluginsList()

  #If the server.log file is changed, a signal connected to this function will be emitted
  def newLineDetected(self):
    thread = GenericThread(self.getNewLines, self.lastServerLine)
    self.disconnect(self, QtCore.SIGNAL('stringFound'), self.routeServerLines)
    self.connect(self, QtCore.SIGNAL('stringFound'), self.routeServerLines)
    thread.start()

  #This function is spawned in the thread to get new lines. It is also called at app spawn
  def getNewLines(self, lastLine):
    newServerLines = self.s.consoleReadTo(lastLine)
    self.emit(QtCore.SIGNAL('stringFound'), newServerLines)

  #This function takes a list of new server lines and routes them to where they need to go.
  def routeServerLines(self, newServerLines):
    chatLines = []
    self.lastServerLine = newServerLines[-1] #Store the last line so we know where to read to later
    for line in newServerLines:
      matchChat = re.search(r'<\w+>', line)
      matchChat2 = re.search(r'\[CONSOLE\]', line)
      matchLoggedIn = re.search(r'(\d+\-\d+\-\d+ \d+:\d+:\d+) \[INFO\] (\w+) \[/(\d+\.\d+\.\d+\.\d+:\d+)\] logged in with entity id (\d+) at', line)
      matchLoggedOut = re.search(r'\] (\w+) lost connection: disconnect.quitting', line)
      matchLoggedOut2 = re.search(r'\] (\w+) lost connection: disconnect.endOfStream', line)
      matchPlugin = re.search(r'\d+\-\d+\-\d+ \d+:\d+:\d+ \[INFO\] \[(\w+)\]', line)

      if matchChat or matchChat2:
        chatLines.append(line)
      
      if matchLoggedIn:
        time = matchLoggedIn.group(1)
        name = matchLoggedIn.group(2)
        ip = matchLoggedIn.group(3)
        ID = matchLoggedIn.group(4)
        self.onlineDict[name] = {'Logged In':time[11:],
                                 'IP':ip,
                                 'ID':ID}
      
      if matchLoggedOut or matchLoggedOut2:
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
    self.updateChatDisplay(chatLines)
    self.updatePlayersDisplay()

  def ticToc(self):
    self.updateStatusBar()

if __name__ == "__main__":
  app = QtGui.QApplication(sys.argv)
  myapp = MyServer()
  myapp.show()
  sys.exit(app.exec_())
