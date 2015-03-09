from PyQt4.QtCore import *
from PyQt4.QtGui import *

import maya.cmds as cmd
import maya.OpenMayaUI as omu
import sip
import os, glob
import shutil
import utilities as amu
import Facade.facade as facade

CHECKOUT_WINDOW_WIDTH = 250
CHECKOUT_WINDOW_HEIGHT = 40

def maya_main_window():
	ptr = omu.MQtUtil.mainWindow()
	return sip.wrapinstance(long(ptr), QObject)


# AddNewAsset is the Dialog window for the add asset button.
class AddNewAsset(QDialog):
	def __init__(self, parent=maya_main_window()):
		#Initialize the GUI
		QDialog.__init__(self, parent)
		self.setWindowTitle('New Asset')
		self.setFixedSize(CHECKOUT_WINDOW_WIDTH, CHECKOUT_WINDOW_HEIGHT)
		self.create_layout()
		self.create_connections()
		
	
	def create_layout(self):
		

		#Create action buttons
		self.addAsset_button = QPushButton('Add Asset')
		self.cancel_button = QPushButton('Cancel')
		
		#Create button layout
		button_layout = QHBoxLayout()
		button_layout.addWidget(self.addAsset_button)
		button_layout.addWidget(self.cancel_button)
		
		#Create main layout
		main_layout = QVBoxLayout()
		main_layout.setSpacing(5)
		main_layout.setMargin(6)
		main_layout.addLayout(button_layout)
		
		self.setLayout(main_layout)

	def create_connections(self):
		
		#Connect the buttons
		self.addAsset_button.clicked.connect(self.new_asset)
		self.cancel_button.clicked.connect(self.close_dialog)
	


	def new_asset(self):
		text, ok = QInputDialog.getText(self, 'New Asset', 'Enter name of new asset (ie: vino)')
		if ok:
			text = str(text)
			print "Trying to create " + text
			facade.newAsset(text)
			#self.refresh()
		

		return

	def close_dialog(self):
		self.close()
		
def go():
	dialog = AddNewAsset()
	dialog.show()
	
if __name__ == '__main__':
	go()
	
	
	
	
	
	
	
	
	
	
