from PyQt4.QtCore import *
from PyQt4.QtGui import *

import os, glob

def getAssetPath(assetName, location):
    if(location == 'Previs'):
        folder = os.environ['PREVIS_DIR']
        assetFolder = 'animation'
    elif(location == 'Model'):
        folder = os.environ['ASSETS_DIR']
        assetFolder = 'model'
    elif(location == 'Rig'):
        folder = os.environ['ASSETS_DIR']
        assetFolder = 'rig'
    elif(location == 'Animation'):
        folder = os.environ['SHOTS_DIR']
        assetFolder = 'animation'
    return os.path.join(folder, assetName, assetFolder)

def getShots():
    return getItems(os.environ['SHOTS_DIR'])
    
def getPrevis():
    return getItems(os.environ['PREVIS_DIR'])
    
def getAssets():
    return getItems(os.environ['ASSETS_DIR'])

def getUserCheckoutDir():
    return os.path.join(os.environ['USER_DIR'], 'checkout')


def getItems(folder):
    tree = QListWidget()
    tree.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
    folders = glob.glob(os.path.join(folder, '*'))
    for f in folders:
        bname = os.path.basename(f)
        item = QListWidgetItem(bname)
        item.setText(bname)
        tree.addItem(item)
    tree.sortItems(0)
    tree.setSortingEnabled(True)
    return tree