import maya.cmds as cmds
import maya_geo_export as geo
import os
import Facade.facade as facade

import maya.OpenMayaUI as omu
import sip
from PyQt4.QtGui import *
from PyQt4.QtCore import *

TAG_GEOMETRY_WIDTH = 340
TAG_GEOMETRY_HEIGHT = 575                                                                                                                                                                   

def maya_main_window():
  ptr = omu.MQtUtil.mainWindow()
  return sip.wrapinstance(long(ptr), QObject)

def setFlag():#facade.getFile(filepath).setFlag(flag)
    print 'set flag'
def getFlag():#get filePath of the maya file and get the flag?#return passToMari
    print 'hey is getting flag'
def saveFile():
    if not cmds.file(q=True, sceneName=True) == '':
        cmds.file(save=True, force=True) #save file

def checkAssetType(givenType):
    # unpack decoded entries and check if the asset type matches what was passed in.
    """ precondition: givenType is either 'model', 'rig', or 'animation' """
    assetName, assetType, version = geo.decodeFileName()
    return assetType == givenType

def saveGeo():
    print 'saving geo to .obj, .bjson'
    # this is not a model asset, don't save objs!
    if not checkAssetType('model'):
        return True
    #print 'we have a model'
    # if we can export the objs, export the objs to the asset folder
    if geo.generateGeometry():
        print 'geo was exported to files.'
        geo.installGeometry()
            
        return True # copy was successful
    else:
        print 'geo was NOT exported to files.'
        return False

def showFailDialog(): 
    return cmds.confirmDialog( title         = 'Checkin Failed'
                             , message       = 'Checkin was unsuccessful'
                             , button        = ['Ok']
                             , defaultButton = 'Ok'
                             , cancelButton  = 'Ok'
                             , dismissString = 'Ok')

def checkin():
    print 'checkin NEW'
    saveFile() # save the file before doing anything
    print 'File saved'

    fileName = cmds.file(q=True, sceneName=True)
    toInstall = checkAssetType('model')
    if not toInstall:
        toInstall = checkAssetType('rig')

    if facade.canCheckin(fileName) and saveGeo(): # objs must be saved before checkin
        print "Can check in."
        comment = 'Comment'
        commentPrompt = cmds.promptDialog(
                  title='Comment',
                  message='What changes did you make?',
                  button=['CheckIn',
                  #'ReadyForShaders',
                  'Cancel'],
                  defaultButton='CheckIn',
                  dismissString='Cancel',
              sf = True)
        if commentPrompt == 'CheckIn':
            comment = cmds.promptDialog(query=True, text=True);
            print "Comment is: " + comment
            saveFile() # One more save
            cmds.file(force=True, new=True) # Open a new file.
            checkinDest = facade.checkin(fileName, comment, toInstall) # checkin, install to stable directories.
        # elif commentPrompt == 'ReadyForShaders':
        #     comment = cmds.promptDialog(query=True, text=True); #setFlag to true so it will always go to check in
        #     print "Comment is: " + comment
        #     saveFile() # One more save
        #     cmds.file(force=True, new=True) # Open a new file.
        #     checkinDest = facade.checkin(fileName, comment, toInstall) # checkin, install to stable directories.
        #     tagGeometry()

        else:
            return

    else:
        showFailDialog()

def tagGeometry():
    print "It worked!!!"
    def __init__(self, parent=maya_main_window()):
      #Setup the different checkout contexts

      #Initialize the GUI
      QDialog.__init__(self, parent)
      self.setWindowTitle('Tag Geometry')
      self.setFixedSize(TAG_GEOMETRY_WIDTH, TAG_GEOMETRY_HEIGHT)
      self.create_layout()
      self.create_connections()
      self.refresh()

    def create_layout(self):
      #Create tabbed view
      self.context_tabs = QTabWidget()
      for context in self.contexts:
        self.context_tabs.addTab(context.tree, context.name)

      #Search input box
      self.search_bar = QLineEdit()
      search_layout = QHBoxLayout()
      search_layout.addWidget(QLabel("Filter: "))
      search_layout.addWidget(self.search_bar)

      #Create Label to hold asset info
      self.asset_info_label = QLabel()
      self.asset_info_label.setWordWrap(True)

      #Create action buttons
      self.new_button = QPushButton('New')
      self.unlock_button = QPushButton('Unlock')
      self.checkout_button = QPushButton('Checkout')
      self.cancel_button = QPushButton('Cancel')
    
      #Create button layout
      button_layout = QHBoxLayout()
      button_layout.setSpacing(2)

      button_layout.addWidget(self.new_button)
      button_layout.addWidget(self.unlock_button)
      button_layout.addStretch()
      button_layout.addWidget(self.checkout_button)
      button_layout.addWidget(self.cancel_button)
    
      #Create main layout
      main_layout = QVBoxLayout()
      main_layout.setSpacing(5)
      main_layout.setMargin(6)
      main_layout.addLayout(search_layout)
      main_layout.addWidget(self.context_tabs)
      main_layout.addWidget(self.asset_info_label)
      main_layout.addLayout(button_layout)
    
      self.setLayout(main_layout)

def go():
    try:
        checkin()
    except Exception as ex:
        msg = "RuntimeException:" + str(ex)
        print msg
        cmds.confirmDialog( title         = 'Uh Oh!'
                          , message       = 'An exception just occured!\r\nHere is the message: ' + msg
                          , button        = ['Dismiss']
                          , defaultButton = 'Dismiss'
                          , cancelButton  = 'Dismiss'
                          , dismissString = 'Dismiss')
