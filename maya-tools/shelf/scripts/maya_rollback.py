from PyQt4.QtCore import *
from PyQt4.QtGui import *

import maya.cmds as cmd
import maya.OpenMayaUI as omu
import sip
import os, glob, shutil
import utilities as amu
import Facade.facade as facade

CHECKOUT_WINDOW_WIDTH = 300
CHECKOUT_WINDOW_HEIGHT = 400

def maya_main_window():
    ptr = omu.MQtUtil.mainWindow()
    return sip.wrapinstance(long(ptr), QObject)

class RollbackDialog(QDialog):
    ORIGINAL_FILE_NAME = cmd.file(query=True, sceneName=True)
    def __init__(self, parent=maya_main_window()):
    #def setup(self, parent):
        self.ORIGINAL_FILE_NAME = cmd.file(query=True, sceneName=True)
        QDialog.__init__(self, parent)
        self.setWindowTitle('Rollback')
        self.setFixedSize(CHECKOUT_WINDOW_WIDTH, CHECKOUT_WINDOW_HEIGHT)
        self.create_layout()
        self.create_connections()
        self.refresh()
  
    def create_layout(self):
        #Create the selected item list
        self.selection_list = QListWidget()
        self.selection_list.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding) 

        #Create Tag, Select, and Cancel buttons
        self.help_button = QPushButton('Help')
        # self.tag_button = QPushButton('Tag')
        self.checkout_button = QPushButton('Checkout')
        self.cancel_button = QPushButton('Cancel')
	
        #Create Label to hold asset info
        self.version_info_label = QLabel("test")
        self.version_info_label.setWordWrap(True)

        #Create button layout
        button_layout = QHBoxLayout()
        button_layout.setSpacing(2)
        button_layout.addStretch()
        # button_layout.addWidget(self.tag_button)
        button_layout.addWidget(self.checkout_button)
        button_layout.addWidget(self.cancel_button)

        #Create main layout
        main_layout = QVBoxLayout()
        main_layout.setSpacing(2)
        main_layout.setMargin(2)
        main_layout.addWidget(self.selection_list)
        main_layout.addWidget(self.version_info_label)
        main_layout.addWidget(self.help_button)
        main_layout.addLayout(button_layout)
        
        self.setLayout(main_layout)

    def create_connections(self):
        #Connect the selected item list widget
        self.connect(self.selection_list,
                    SIGNAL('currentItemChanged(QListWidgetItem*, QListWidgetItem*)'),
                    self.set_current_item)
            
        #Connect the buttons
        self.connect(self.help_button, SIGNAL('clicked()'), self.help_dialog)
        #self.connect(self.tag_button, SIGNAL('clicked()'), self.rename_tagged_version)
        self.connect(self.checkout_button, SIGNAL('clicked()'), self.checkout_version)
        self.connect(self.cancel_button, SIGNAL('clicked()'), self.close_dialog)
	
    def update_selection(self, selection):
        #Remove all items from the list before repopulating
        self.selection_list.clear()
        self.version_info_label.clear()

        #Add the list to select from
        for s in selection:
            item = QListWidgetItem(s)
            item.setText(s)
            self.selection_list.addItem(item)
        self.selection_list.sortItems(0)

    def refresh(self):	
        selections = facade.getAssetVersions(self.ORIGINAL_FILE_NAME)
        self.update_selection(selections)

    def get_checkout_mode(self):
        return ''

    ########################################################################
    # SLOTS
    ########################################################################
    def close_dialog(self):
        print self.ORIGINAL_FILE_NAME
        # cmd.file(self.ORIGINAL_FILE_NAME, force=True, open=True)
        self.close()

    def set_current_item(self, item):
        self.current_item = item
        self.show_version_info()

    def show_no_file_dialog(self):
        return cmd.confirmDialog(  title           = 'No Such Version'
                                   , message       = 'For some reason this version folder does not contain a file. Please try another version.'
                                   , button        = ['Ok']
                                   , defaultButton = 'Ok'
                                   , cancelButton  = 'Ok'
                                   , dismissString = 'Ok')

    def verify_checkout_dialog(self):
        return cmd.confirmDialog(  title           = 'Verify Checkout'
                                   , message       = 'You are about to checkout an older version of this asset. If you have made changes to your currently checked out file, they will be lost.  Is this OK?'
                                   , button        = ['Yes', 'No']
                                   , defaultButton = 'No'
                                   , cancelButton  = 'No'
                                   , dismissString = 'No')

    def help_dialog(self):
        return cmd.confirmDialog(  title           = 'Help'
                                   , message       = 'CHECKOUT: Checks out the selected version so you can modify it. when you check it in, it will be saved as the newest version.\n If you have made changes to your currently checked out file, you should check those in first'
                                   , button        = ['Ok']
                                   , defaultButton = 'Ok'
                                   , cancelButton  = 'Ok'
                                   , dismissString = 'Ok')
# This didn't work before but we could do once eveything has been updated. We could change the name of the version that way we won't need to look at description before rolling back
#    def rename_tagged_version(self):
#        return cmd.promptDialog(  title           = 'Tagg it like its hot'
#                                   , message       = 'Choose a good naming convention. Something you will remember... Forrrreeeeverrrrrr'
#                                   , button        = ['Done' , 'NVM']
#				   , defaultButton = 'Done'
#                                )
#        if result == 'Done':
#       	    taggedVersion = cmd.promptDialog(query=True, text=True)

    # def open_version(self):
    #     dialogResult = self.verify_open_version_dialog()
    #     if (dialogResult == 'Ok'):
    #         filePath = os.path.join(amu.getUserCheckoutDir(), os.path.basename(os.path.dirname(self.ORIGINAL_FILE_NAME)))
    #         checkInDest = amu.getCheckinDest(filePath)
    #         v = str(self.current_item.text())
    #         checkinPath = os.path.join(checkInDest, "src", v)
    #         checkinName = os.path.join(checkinPath, os.path.basename(self.ORIGINAL_FILE_NAME))
    #         print checkinName
    #         if os.path.exists(checkinName):
    #             cmd.file(checkinName, force=True, open=True)
    #         else:
    #             self.show_no_file_dialog()

    def checkout_version(self):
        dialogResult = self.verify_checkout_dialog()
        if(dialogResult == 'Yes'):
            # TODO: I would love to clean this up so Maya doesn't have to be aware of the guts of the asset manager. Big question is the exception. Can we do this otherwise?
            versionToCheckout = str(self.current_item.text())[1:]
            
            # So we first discard, then try to checkout the asset, move the version number so now it's pointing the the next one, and THEN we checkout that one.
            assetType = facade.getAssetType(self.ORIGINAL_FILE_NAME)
            assetName = facade.getAssetName(self.ORIGINAL_FILE_NAME)

            print "assetType, assetName: ", assetType, assetName

            toCheckout = facade.getCheckinDest(self.ORIGINAL_FILE_NAME) # I would like to push this into the asset manager eventually.

            latestVersion = amu.tempSetVersion(toCheckout, versionToCheckout)
            print "latest version: ", latestVersion
            facade.discard(self.ORIGINAL_FILE_NAME) 
            try:
                destpath = facade.checkout(assetName, True, assetType) 
            except Exception as e:
                if not facade.checkedOutByMe(assetName, assetType):
                    cmd.confirmDialog(  title          = 'Can Not Checkout'
                                   , message       = str(e)
                                   , button        = ['Ok']
                                   , defaultButton = 'Ok'
                                   , cancelButton  = 'Ok'
                                   , dismissString = 'Ok')
                    return
                else:
                    destpath = facade.getCheckoutDest(assetName, assetType)

            amu.tempSetVersion(toCheckout, latestVersion)
            # move to correct checkout directory
            correctCheckoutDir = facade.getCheckoutDest(assetName, assetType)
            fileName = facade.rollback(self.ORIGINAL_FILE_NAME, assetName, assetType, destpath)

            toOpen = fileName +'.mb'
            self.ORIGINAL_FILE_NAME = toOpen
            if not os.path.exists(toOpen):
                # create new file
                cmd.file(force=True, new=True)
                cmd.file(rename=toOpen)
                cmd.file(save=True, force=True)
            cmd.file(self.ORIGINAL_FILE_NAME, force=True, open=True)
            self.close_dialog()

    def show_version_info(self):
        asset_version = str(self.current_item.text())
        comment = facade.getVersionComment(asset_version, self.ORIGINAL_FILE_NAME)
        self.version_info_label.setText(comment)
   
def go():
    currentFile = cmd.file(query=True, sceneName=True)
    filePath = os.path.join(amu.getUserCheckoutDir(), os.path.basename(os.path.dirname(currentFile)))
    if(amu.isCheckedOutCopyFolder(filePath)):
        cmd.file(save=True, force=True)
        dialog = RollbackDialog()
        dialog.show()
    else:
        cmd.confirmDialog(  title         = 'Invalid Command'
                           , message       = 'This is not a checked out file. There is nothing to rollback.'
                           , button        = ['Ok']
                           , defaultButton = 'Ok'
                           , cancelButton  = 'Ok'
                           , dismissString = 'Ok')
    
if __name__ == '__main__':
    go()
    
