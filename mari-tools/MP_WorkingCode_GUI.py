# Coded by Andrew Rasmussen 2013. When it is terrible or breaks blame him. Or bake him pity cookies.
#Pop Up Gui and Shelf Gui
# ------------------------------------------------------------------------------



# LOOK HERE
# Not sure why this WorkingCode_GUI and WorkingCode are in here. I'm going to try sticking with only one.
# When I comment one or the other out, we don't get the full thing in here. Can we combine?


import os
import mari
import random
import PythonQt.QtGui as gui
#import MP_WorkingCode_archiveAsset
#import MP_WorkingCode_AssetInfo
#import MP_WorkingCode_exportMaps
import MP_WorkingCode_mariProjCreate as pc
#import MP_WorkingCode_OBJUpdate
#import MP_WorkingCode_saveAll
#import MP_WorkingCode_turnTableRender

MARI_DEFAULT_GEOMETRY_PATH = os.environ['MARI_DEFAULT_GEOMETRY_PATH']

# ------------------------------------------------------------------------------
def DSPAssetInfo():
	printInfoList = mari.projects.list()
	print "--------------------------------------"
	print (printInfoList)
	print "--------------------------------------"
# ------------------------------------------------------------------------------
mainPal = mari.palettes.create("BYU Mari Tools", "BYU Mari Tools") # As of 2.6, this requires a QWidget to be passed in.
widget = gui.QWidget()
widget.resize(150, 275)
mainPal.setBodyWidget(widget)
layout = gui.QVBoxLayout()
widget.setLayout(layout)
layout.addWidget(gui.QLabel("Welcome to the uber palette."))

# ------------------------------------------------------------------------------
#ButtonCreation
createProjectPB = gui.QPushButton("Create Project")
layout.addWidget(createProjectPB)
connect(createProjectPB.clicked, pc.mariProjectCreate)

changeExportPathPB = gui.QPushButton("Change Export Path for Project")
layout.addWidget(changeExportPathPB)
connect(changeExportPathPB.clicked, changeExportPath)

ExportSelMapPB = gui.QPushButton("Export Selected Map")
layout.addWidget(ExportSelMapPB)
connect(ExportSelMapPB.clicked, exportSelectedMaps)

ExportAllMapsPB = gui.QPushButton("Export All Maps")
layout.addWidget(ExportAllMapsPB)
connect(ExportAllMapsPB.clicked, exportAllMaps)

AssetInfoPB = gui.QPushButton("Display Asset Info")
layout.addWidget(AssetInfoPB)
connect(AssetInfoPB.clicked, DSPAssetInfo)

# ------------------------------------------------------------------------------
mainPal.show
widget.resize(225, 275)
